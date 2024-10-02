StreamForge : Real-Time Data Pipeline with Machine Learning and Blockchain Integration

Table of Contents
Project Overview
Architecture
Technologies
Project Setup
Key Components
Usage
Contributing
License
Project Overview
This project is a Real-Time Data Pipeline that integrates machine learning models and blockchain technology. The pipeline enables real-time data ingestion, transformation, and analytics using Kafka, Cassandra, Apache Airflow, and Postgres as key components. It demonstrates how businesses can use machine learning models to gain insights and blockchain for secure and transparent data tracking.

Key Features:
Real-Time Data Processing with Kafka and Cassandra.
Machine Learning Integration for predictive analytics.
Blockchain for immutable and decentralized ledger tracking.
Apache Airflow for workflow orchestration.
PostgreSQL as the metadata database for Airflow.
Architecture

The architecture consists of:

Kafka: Streams real-time data between producers and consumers.
Cassandra: A NoSQL database for scalable and fast data storage.
Postgres: Backend for storing Airflow metadata.
Apache Airflow: For scheduling and managing the pipeline workflows.
Docker: Containerized environment for easy deployment.
Technologies
Technology	Version	Description
Apache Kafka	3.3.2	Real-time data streaming and pub/sub system
Cassandra	4.0	Distributed NoSQL database for fast, scalable storage
Apache Airflow	2.6.2	Workflow orchestration and pipeline management
PostgreSQL	13	Relational database for Airflow metadata storage
Docker Compose	3.8	Container orchestration for development environments
Project Setup
Prerequisites
Ensure you have the following installed:

Docker and Docker Compose: Install Docker
Python 3.10 (for managing Python dependencies and running DAGs locally, if necessary)
Installation Steps
Clone the repository:

bash
Copy code
git clone https://github.com/Atharv-Nanaware/StreamForge.git
cd StreamForge
Environment Configuration: Ensure you have the correct .env file for configuring environment variables:

bash
Copy code
cp .env.example .env
Install Python dependencies:

bash
Copy code
pip install -r requirements.txt
Start the Docker Containers:

bash
Copy code
docker-compose up -d
Initialize the Airflow Database:

bash
Copy code
docker-compose run airflow-init
Access Airflow UI: Open a browser and go to http://localhost:8080. Use the default credentials:

Username: admin
Password: admin
Stopping the Containers
To stop all services:

bash
Copy code
docker-compose down
Key Components
Kafka
Topic Management: Kafka is responsible for streaming data between different services. It enables producers to publish data to Kafka topics, while consumers read data from those topics in real time.
Cassandra
Data Storage: Cassandra handles the real-time data ingestion at scale. It stores all the processed and raw data from the Kafka streams, enabling high-throughput and low-latency data access.
Apache Airflow
Pipeline Orchestration: Airflow schedules the workflow that ingests data from Kafka, processes it using Python operators, and stores the results in Cassandra and Postgres. It also integrates with machine learning models for batch predictions.
PostgreSQL
Metadata Store: Airflow uses PostgreSQL as a metadata database to track DAG runs, tasks, and results.
Usage
Running DAGs
After setting up the environment, navigate to the Airflow UI at http://localhost:8080.
You can enable/trigger your DAGs from the UI.
Monitor DAG runs, task status, logs, and visualize task dependencies from the UI.
Accessing Kafka
You can interact with the Kafka service using a CLI or a client like kafka-python or confluent-kafka-python.

Cassandra Querying
Once the pipeline has ingested data into Cassandra, you can query the database using CQL (Cassandra Query Language). For example:

bash
Copy code
docker exec -it <cassandra-container-id> cqlsh
Contributing
Contributions are welcome! Follow these steps to contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/my-feature).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature/my-feature).
Open a Pull Request.
Coding Guidelines
Follow PEP 8 standards for Python code.
Ensure all DAGs and scripts are tested before submission.
License
This project is licensed under the MIT License - see the LICENSE file for details.

