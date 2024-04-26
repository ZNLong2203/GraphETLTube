import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import pyspark.sql.functions as F

def create_table(conn, cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS edges (
            prev_node INTEGER REFERENCES nodes(id),
            next_node INTEGER REFERENCES nodes(id),
            relationship VARCHAR(255) NOT NULL,
            PRIMARY KEY (prev_node, next_node) 
        )
    """)
    conn.commit()

def insert_data(conn, cur):
    cur.execute("""
        INSERT INTO nodes (name)
        VALUES ('A'), ('B'), ('C'), ('D'), ('E')
    """)

    cur.execute("""
        INSERT INTO edges (prev_node, next_node, relationship)
        VALUES (1, 2, 'friend'), (1, 3, 'enemy'), (2, 3, 'friend'), (3, 4, 'friend'), (4, 5, 'enemy')
    """)
    conn.commit()

if __name__ == '__main__':
    conn = psycopg2.connect(
        host='localhost',
        dbname='graph',
        user='postgres',
        password='postgres'
    )
    cur = conn.cursor()

    create_table(conn, cur)
    insert_data(conn, cur)
