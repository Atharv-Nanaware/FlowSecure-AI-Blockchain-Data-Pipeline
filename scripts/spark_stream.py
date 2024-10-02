import logging
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, sha2, concat_ws
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.ml import PipelineModel
from web3 import Web3

def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)
    print("Keyspace created successfully!")

def create_table(session):
    session.execute("""
    CREATE TABLE IF NOT EXISTS spark_streams.created_users (
        id UUID PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        address TEXT,
        post_code TEXT,
        email TEXT,
        username TEXT,
        dob TEXT,
        registered_date TEXT,
        phone TEXT,
        picture TEXT,
        prediction TEXT,
        data_hash TEXT
    );
    """)
    print("Table created successfully!")

def create_spark_connection():
    s_conn = None
    try:
        s_conn = SparkSession.builder \
            .appName('SparkDataStreaming') \
            .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.13:3.4.1,"
                                           "org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.1") \
            .config('spark.cassandra.connection.host', 'localhost') \
            .getOrCreate()

        s_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connection created successfully!")
    except Exception as e:
        logging.error(f"Couldn't create the spark session due to exception {e}")

    return s_conn

def connect_to_kafka(spark_conn):
    spark_df = None
    try:
        spark_df = spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'localhost:9092') \
            .option('subscribe', 'users_created') \
            .option('startingOffsets', 'latest') \
            .load()
        logging.info("Kafka DataFrame created successfully")
    except Exception as e:
        logging.warning(f"Kafka DataFrame could not be created because: {e}")

    return spark_df

def create_cassandra_connection():
    from cassandra.cluster import Cluster
    try:
        # Connecting to the Cassandra cluster
        cluster = Cluster(['localhost'])
        cas_session = cluster.connect()
        return cas_session
    except Exception as e:
        logging.error(f"Could not create Cassandra connection due to {e}")
        return None

def create_selection_df_from_kafka(spark_df):
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("address", StringType(), False),
        StructField("post_code", StringType(), False),
        StructField("email", StringType(), False),
        StructField("username", StringType(), False),
        StructField("dob", StringType(), False),
        StructField("registered_date", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("picture", StringType(), False)
    ])

    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col('value'), schema).alias('data')).select("data.*")
    print(sel)

    return sel

def init_blockchain():
    # Initialize blockchain connection
    blockchain_url = os.getenv('BLOCKCHAIN_URL')  # Ensure this is set in your environment
    web3 = Web3(Web3.HTTPProvider(blockchain_url))
    if web3.isConnected():
        logging.info("Connected to Blockchain!")
    else:
        logging.error("Blockchain connection failed.")
        raise Exception("Blockchain connection failed.")
    return web3

def log_hash_to_blockchain(web3, data_hash):
    # Function to log data hash to blockchain
    # Placeholder for blockchain transaction code
    try:
        # Example: Sending a transaction to log the data hash
        tx_hash = web3.eth.sendTransaction({
            'from': web3.eth.accounts[0],
            'to': web3.eth.accounts[1],
            'value': 0,
            'data': web3.toHex(text=data_hash)
        })
        logging.info(f"Logged data hash to blockchain with transaction hash: {tx_hash.hex()}")
    except Exception as e:
        logging.error(f"Failed to log data hash to blockchain: {e}")

def process_batch(batch_df, batch_id):
    logging.info(f"Processing batch {batch_id}")

    # Load machine learning model
    model_path = os.getenv('MODEL_PATH')  # Ensure this is set in your environment
    model = PipelineModel.load(model_path)

    # Apply the model to the batch data
    predictions_df = model.transform(batch_df)

    # Compute data hash
    predictions_df = predictions_df.withColumn('data_hash', sha2(concat_ws('||', *predictions_df.columns), 256))

    # Initialize blockchain connection
    web3 = init_blockchain()

    # Log data hashes to blockchain
    data_hashes = predictions_df.select('data_hash').collect()
    for row in data_hashes:
        data_hash = row['data_hash']
        log_hash_to_blockchain(web3, data_hash)

    # Write the predictions to Cassandra
    predictions_df.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(keyspace="spark_streams", table="created_users") \
        .save()

if __name__ == "__main__":
    # Create Spark connection
    spark_conn = create_spark_connection()

    if spark_conn is not None:
        # Connect to Kafka with Spark connection
        spark_df = connect_to_kafka(spark_conn)
        selection_df = create_selection_df_from_kafka(spark_df)
        session = create_cassandra_connection()

        if session is not None:
            create_keyspace(session)
            create_table(session)

            logging.info("Streaming is being started...")

            streaming_query = (selection_df.writeStream
                               .foreachBatch(process_batch)
                               .start())

            streaming_query.awaitTermination()
