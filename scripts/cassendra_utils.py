from cassandra.cluster import Cluster

def create_keyspace_and_table():
    cluster = Cluster(['localhost'])
    session = cluster.connect()

    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    """)

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
            picture TEXT);
    """)

if __name__ == "__main__":
    create_keyspace_and_table()
