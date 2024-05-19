import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import pyspark.sql.functions as F

def create_table(conn, cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255), 
            description VARCHAR(255)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS edges (
            prev_node INTEGER REFERENCES nodes(id),
            next_node INTEGER REFERENCES nodes(id),
            relationship VARCHAR(255),
            PRIMARY KEY (prev_node, next_node) 
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS node_program (
            id SERIAL PRIMARY KEY,
            project_id VARCHAR(255),
            submitter_id VARCHAR(255),
            program_name VARCHAR(255)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS node_information (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            age INTEGER,
            dob DATE,
            address VARCHAR(255),
            phone VARCHAR(255)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS node_allergy (
            id SERIAL PRIMARY KEY,
            allergy_1 VARCHAR(255),
            allergy_2 VARCHAR(255),
            allergy_3 VARCHAR(255),
            description VARCHAR(255)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS node_medical_history (
            id SERIAL PRIMARY KEY,
            disease_1 VARCHAR(255),
            disease_2 VARCHAR(255),
            disease_3 VARCHAR(255),
            description VARCHAR(255)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS node_report (
            id SERIAL PRIMARY KEY,
            description VARCHAR(255)
        )
    """)

    conn.commit()

def insert_data(conn, cur):
    cur.execute("""
        INSERT INTO nodes (name)
        VALUES ('node_program'), ('node_information'), ('node_allergy'), ('node_medical_history'), ('node_report')
    """)

    cur.execute("""
        INSERT INTO edges (prev_node, next_node, relationship)
        VALUES (1, 2, 'required'), (1, 3, 'required'), (2, 3, 'required'), (3, 4, 'required'), (4, 5, 'required')
    """)
    conn.commit()

def insert_node(conn, cur):
    cur.execute("""
        INSERT INTO node_program (project_id, submitter_id, program_name)
        VALUES ('WEGMIW234', 'BMOTRHOTKR42', 'Test')
    """)

    cur.execute("""
        INSERT INTO node_information (name, age, dob, address, phone)
        VALUES ('Nguyen Van A', 20, '2000-01-01', 'Ha Noi', '0123456789')
    """)

    cur.execute("""
        INSERT INTO node_allergy (allergy_1, allergy_2, allergy_3, description)
        VALUES ('Weather', 'Beef', 'Essential oil', Null)
    """)

    cur.execute("""
        INSERT INTO node_medical_history (disease_1, disease_2, disease_3, description)
        VALUES ('Fever', 'Headache', 'Tired', Null)
    """)

    cur.execute("""
        INSERT INTO node_report (description)
        VALUES ('Have many allergies')
    """)

    conn.commit()

if __name__ == '__main__':
    conn = psycopg2.connect(
        host='localhost',
        dbname='postgres',
        user='postgres',
        password='test'
    )
    cur = conn.cursor()

    create_table(conn, cur)
    insert_data(conn, cur)
    insert_node(conn, cur)
