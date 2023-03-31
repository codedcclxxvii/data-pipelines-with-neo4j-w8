## Documentation

This data pipeline extracts data from a Neo4j graph database, transforms it using pandas, and loads it into a PostgreSQL database.
The goal is to optimize the business processes of a telecommunications company by allowing for easier querying and analysis of their customer,
subscription, and service data.

### Setting Up

Install the necessary dependencies by running pip install -r requirements.txt.

Create a .env file in the root directory of the project and set the following environment variables:


    NEO4J_URI: the URI of the Neo4j database

    NEO4J_USERNAME: the username for the Neo4j database

    NEO4J_PASSWORD: the password for the Neo4j database

    PGDATABASE: the name of the PostgreSQL database

    PGUSER: the username for the PostgreSQL database

    PGPASSWORD: the password for the PostgreSQL database

    PGHOST: the host of the PostgreSQL database

    PGPORT: the port of the PostgreSQL database

Make sure that the Neo4j database is running and accessible.

Create a PostgreSQL database with the name telecom.

Create a virtual environment and activate it by running the following commands

python3 -m venv env
source env/bin/activate

Run the data pipeline by running python main.py.

### Data Schema

The data schema for the PostgreSQL database is as follows:
CREATE TABLE subscriptions (
    customer_id INTEGER,
    subscription_id INTEGER,
    service_id INTEGER,
    start_date DATE,
    end_date DATE,
    price FLOAT
);

### Transformations

The data is transformed using pandas to clean and manipulate the extracted data from Neo4j. The following transformations are performed:

The start_date and end_date fields are converted from strings to datetime objects.

Null values are removed from the DataFrame.

The price field is rounded to two decimal places.

### Limitations

This data pipeline is designed to work with a specific Neo4j graph database schema and a specific PostgreSQL database schema.
It may require modifications to work with different schemas. Additionally, the data pipeline is not optimized for large datasets
and may perform slowly or run out of memory if the dataset is too large.
