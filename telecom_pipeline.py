import neo4j
import pandas as pd
import psycopg2


def extract_neo4j_data(uri, username, password):
    """
    Extract data from Neo4j database using Cypher query
    """
    query = """
    MATCH (c:Customer)-[s:SUBSCRIBES_TO]->(svc:Service)
    RETURN c.customer_id, s.subscription_id, svc.service_id,
           s.start_date, s.end_date, s.price
    """
    with neo4j.GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            results = session.run(query)
            data = results.data()
    return data


def transform_neo4j_data(data):
    """
    Transform data using Pandas DataFrame
    """
    df = pd.DataFrame(data)
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df.dropna(inplace=True)
    return df


def load_postgres_data(df, host, port, dbname, user, password, table_name):
    """
    Load data into Postgres database
    """
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            customer_id INTEGER,
            subscription_id INTEGER,
            service_id INTEGER,
            start_date DATE,
            end_date DATE,
            price FLOAT
        )
    """
    cursor.execute(create_table_query)

    for _, row in df.iterrows():
        insert_query = f"""
            INSERT INTO {table_name} (customer_id, subscription_id, service_id, start_date, end_date, price)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            row['customer_id'], row['subscription_id'], row['service_id'],
            row['start_date'], row['end_date'], row['price']
        ))

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    # Extract data from Neo4j
    neo4j_uri = 'bolt://localhost:7687'
    neo4j_username = 'neo4j'
    neo4j_password = 'password'
    data = extract_neo4j_data(neo4j_uri, neo4j_username, neo4j_password)

    # Transform data using Pandas
    df = transform_neo4j_data(data)

    # Load data into Postgres
    postgres_host = 'localhost'
    postgres_port = 5432
    postgres_dbname = 'telecom'
    postgres_user = 'postgres'
    postgres_password = 'password'
    table_name = 'subscriptions'
    load_postgres_data(df, postgres_host, postgres_port, postgres_dbname, postgres_user, postgres_password, table_name)
