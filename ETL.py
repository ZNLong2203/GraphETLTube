import datetime
import re
import psycopg2
import json
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from datetime import date
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import pyspark.sql.functions as F

def find_all_path(conn, cur, start_node, end_node):
    cur.execute("""
          WITH RECURSIVE traversed(path, node_id) AS (
            SELECT ARRAY[prev_node] AS path, next_node AS node_id
            FROM edges
            WHERE prev_node = %s

            UNION ALL

            SELECT traversed.path || edges.prev_node, edges.next_node
            FROM traversed
            JOIN edges ON edges.prev_node = traversed.node_id
            WHERE edges.next_node != ANY(traversed.path)
        )
        SELECT path || node_id AS path
        FROM traversed
        WHERE node_id = %s;
    """, (start_node, end_node)
    )
    ## 1. Create array of path and add the start node
    ## 2. Find the next node from the edges table
    ## 3. Join the traversed table with edges table
    ## 4. Loai bo chu trinh
    ## 5. Choose the path that has the end node
    conn.commit()
    rows = cur.fetchall()

    return rows

def distinct_id(rows):
    distinct = set()
    for row in rows:
        for i in range(len(row[0])):
            distinct.add(row[0][i])
    return distinct

def json_format(conn, cur, distinct):
    data_dict = {}
    tbl_dict = {}
    tmp_delete = list(distinct)
    tmps = list(distinct)

    # Remove the optional relationship that connect to the end node
    for i in range(len(tmp_delete) - 1):
        cur.execute("""
            SELECT relationship FROM edges WHERE prev_node = %s AND next_node = %s
        """, (tmp_delete[i], tmps[-1]))
        relationship = cur.fetchone()
        if relationship == "optional":
            tmps.remove(tmp_delete[i])

    # Select the end node as the key
    cur.execute("""
        SELECT name FROM nodes WHERE id = %s
    """, (tmps[-1],))

    end_node = cur.fetchone()[0]  # Retrieve the result
    end_node = end_node[5:]  # Remove the "node_" prefix

    for i in range(len(tmps) - 1):
        # Select each node (table name)
        cur.execute("""
            SELECT  name FROM nodes WHERE id = %s
        """, (tmps[i],))
        node = cur.fetchone()[0]

        # Select all the data from the table
        cur.execute("""
            SELECT * FROM {}
        """.format(node)
        )
        data = cur.fetchone()

        # Get the column headers
        column_headers = [desc[0] for desc in cur.description]
        column_headers = column_headers[1:]
        # print(column_headers)

        tmp = {}
        for j in range(len(data) - 1):
            tmp[column_headers[j]] = data[j+1]

        node = node[5:]
        tbl_dict[node] = tmp

    data_dict[end_node] = tbl_dict
    print(data_dict)
    return data_dict

def export_json(data_dict):
    # Define a default serializer for the json.dumps() function
    def default_serializer(obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    # Convert data_dict to a list of tuples
    data_tuples = [(json.dumps({key: value}, indent=4, default=default_serializer),) for key, value in data_dict.items()]

    # Write to json file
    with open('data.json', 'w') as f:
        for data in data_tuples:
            f.write(data[0] + '\n')

if __name__ == '__main__':
    # Create a connection to the postgres database
    conn = psycopg2.connect(
        host='localhost',
        dbname='postgres',
        user='postgres',
        password='test'
    )
    cur = conn.cursor()

    rows = find_all_path(conn, cur, 1, 5)
    distinct = distinct_id(rows)
    data_dict = json_format(conn, cur, distinct)
    export_json(data_dict)

