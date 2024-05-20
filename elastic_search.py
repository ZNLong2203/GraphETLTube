from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create Spark session
spark = SparkSession.builder \
    .appName("Load JSON to Elasticsearch") \
    .config("spark.es.nodes", "localhost") \
    .config("spark.es.port", "9200") \
    .config("spark.es.nodes.wan.only", "true") \
    .getOrCreate()

# Set log level to ERROR to reduce log verbosity
spark.sparkContext.setLogLevel("ERROR")

# Read the JSON data from file into a DataFrame
df = spark.read.option("multiline", "true").json("data.json")

# Inspect the schema to ensure it is loaded correctly
df.printSchema()
df.show(truncate=False)

# Extract the fields in the order they appear in the JSON
fields = df.schema["node_report"].dataType.fields

# Dynamically select columns in the exact order they appear in the JSON
df_flat = df.select([col(f"node_report.{field.name}").alias(field.name) for field in fields])

# Print flattened DataFrame schema and content for debugging
df_flat.printSchema()
df_flat.show(truncate=False)

# Write the flattened DataFrame to Elasticsearch
df_flat.write \
    .format("org.elasticsearch.spark.sql") \
    .option("es.resource", "test") \
    .option("es.nodes", "localhost") \
    .option("es.port", "9200") \
    .mode("overwrite") \
    .save()

# Stop the Spark session
spark.stop()
