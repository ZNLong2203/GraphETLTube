import psycopg2
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
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
    # for row in rows:
    #     print(row[0])

    return rows

def distinct_id(rows):
    distinct = set()
    for row in rows:
        for i in range(len(row[0])):
            distinct.add(row[0][i])
    # print(distinct)
    return distinct

def export_json(conn, cur, distinct):
    data_dict = {}
    tmps = list(distinct)
    df = pd.DataFrame(tmps, columns=['id'])
    print(df)
    # for tmp in tmps:
    #     cur.execute("""
    #         SELECT *
    #         FROM nodes
    #         WHERE id = %s
    #     """, (str(tmp))
    #     )
    #     row = cur.fetchone()
    #     data_dict[str(tmp)] = row[1]
    #
    # conn.commit()
    # print(data_dict)

if __name__ == '__main__':
    conn = psycopg2.connect(
        host='localhost',
        dbname='graph',
        user='postgres',
        password='postgres'
    )
    cur = conn.cursor()

    rows = find_all_path(conn, cur, 1, 5)
    distinct = distinct_id(rows)
    export_json(conn, cur, distinct)
