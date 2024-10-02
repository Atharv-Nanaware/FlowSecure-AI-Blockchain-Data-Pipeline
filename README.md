RealTimeDataPipeline/
│
├── config/
│   └── cassandra_schema.cql     # Cassandra schema definition
│
├── dags/
│   └── user_data_pipeline.py    # Airflow DAG with Kafka producer and blockchain integration
│
├── scripts/
│   ├── kafka_producer.py        # Kafka producer script (already provided)
│   ├── spark_streaming.py       # Spark Streaming script to read from Kafka and write to Cassandra
│   └── cassandra_utils.py       # Utility functions for Cassandra setup
│
├── docker-compose.yml           # Docker Compose for Kafka, Zookeeper, and Cassandra
├── logs/
│   └── streaming.log            # Logs for the Spark Streaming app
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
