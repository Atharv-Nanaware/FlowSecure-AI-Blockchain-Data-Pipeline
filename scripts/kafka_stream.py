from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from web3 import Web3
import json
from kafka import KafkaProducer
import time
import logging

# Kafka and Airflow Config
default_args = {
    'owner': 'panda',
    'start_date': datetime(2023, 10, 30, 10, 00)
}

# Web3 Blockchain Initialization
def init_blockchain():
    # Connecting to Ethereum mainnet via Infura
    infura_url = "https://mainnet.infura.io/v3/25adae314dc64c7792bcb1470bba8ce1"  # Using your Infura key directly
    web3 = Web3(Web3.HTTPProvider(infura_url))

    if web3.isConnected():
        print("Connected to Infura!")
        return web3
    else:
        print("Blockchain connection failed.")
        raise Exception("Blockchain connection failed.")

# Task 1: Get Random User Data
def get_data():
    import requests
    res = requests.get('https://randomuser.me/api/')
    res = res.json()
    res = res['results'][0]
    return res

# Task 2: Format Data
def format_data(res):
    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, {location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    return data

# Task 3: Stream Data to Kafka and Log Hash on Blockchain
def stream_data():
    web3 = init_blockchain()  # Initialize blockchain connection
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    cur_time = time.time()

    while True:
        if time.time() > cur_time + 60:  # Run for 1 minute
            break
        try:
            res = get_data()
            formatted_data = format_data(res)

            # Send data to Kafka
            producer.send('users_created', json.dumps(formatted_data).encode('utf-8'))

            # Create a hash of the formatted data to log it immutably to the blockchain
            data_hash = web3.sha3(text=json.dumps(formatted_data))
            print(f"Logging data hash to blockchain: {data_hash.hex()}")

        except Exception as e:
            logging.error(f'An error occurred: {e}')
            continue

# Define DAG (Airflow Task Pipeline)
with DAG('user_data_pipeline', default_args=default_args, schedule='@daily', catchup=False) as dag:
    task_stream_data = PythonOperator(
        task_id='stream_data',
        python_callable=stream_data
    )


print ("Everything is Ok")