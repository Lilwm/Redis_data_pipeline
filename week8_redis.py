# -*- coding: utf-8 -*-
"""Week8_Redis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w7J0n1G4wygHSkaqRKKVn4wLg6QKdFne
"""

!pip install redis

import pandas as pd
import redis
import psycopg2

# Redis configuration

redis_host ='redis-15919.c91.us-east-1-3.ec2.cloud.redislabs.com'
redis_port = 15919
redis_password ='nVmHZlngfY9h61SwlkrcIsk8VF4ukWe4'

# PostgreSQL configuration
pg_host = 'localhost'
pg_database = 'call_logs'
pg_user = 'Admin_1'
pg_password = 'Admin'

#filename
filename ='customer_call_logs.csv'

# Redis client
redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

def extract_data():
    # Extract data from CSV file using pandas
    df = pd.read_csv('customer_call_logs.csv')
    
    # Cache data in Redis for faster retrieval
    redis_client.set('customer_call_logs', df.to_json())
    return df

def transform_data():
    # Retrieve data from Redis cache
    data = pd.read_json(redis_client.get('customer_call_logs').decode('utf-8'))
    print(data)
    transformed_data = pd.DataFrame({
        'customer_id': data['customer_id'],
        'call_cost_usd': data['call_cost'].str.strip('$'),
        'call_destination': data['call_destination'],
        'call_date': pd.to_datetime(data['call_date']),
        'call_duration_min': pd.to_timedelta(data['call_duration']).astype('timedelta64[m]')
    })
    return(transformed_data)

def load_data(transformed_data):
    # Connect to Postgres database
    conn = psycopg2.connect(host=pg_host,  port=5432, database=pg_database, user=pg_user, password=pg_password)

    # Create a cursor object
    cur = conn.cursor()

    # Create a table to store the data
    cur.execute('CREATE TABLE IF NOT EXISTS customer_call_logs (\
                 customer_id INT,\
                 call_cost_usd FLOAT,\
                 call_destination VARCHAR,\
                 call_date TIMESTAMP,\
                 call_duration_min FLOAT\
                 )')

    # Insert the transformed data into the database
    for i, row in transformed_data.iterrows():
        cur.execute(f"INSERT INTO customer_call_logs (customer_id, call_cost_usd, call_destination, call_date, call_duration_min) VALUES ({row['customer_id']}, {row['call_cost_usd']}, '{row['call_destination']}', '{row['call_date']}', {row['call_duration_min']})")

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

def data_pipeline():
    # Data pipeline function
    extract_data()
    transformed_data = transform_data(transformed_data)
    load_data(transformed_data)

if __name__ == '__main__':
    # Run the data pipeline function
    data_pipeline()