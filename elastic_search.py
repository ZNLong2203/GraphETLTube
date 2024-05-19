from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
from pyspark.sql.functions import from_json

if __name__ == "__main__":
    # Initialize Spark session
    spark = (SparkSession.builder.appName("ElasticSearch")
             .master("local")
             .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:8.13.4")
             .config("spark.es.nodes", "localhost")
             .config("spark.es.port", "9200")
             .config("spark.es.nodes.wan.only", "true")
             .getOrCreate())

    # Define schema for the inner "node_report" object
    schema = StructType([
        StructField("project_id", StringType(), True),
        StructField("submitter_id", StringType(), True),
        StructField("program_name", StringType(), True),
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("dob", StringType(), True),
        StructField("address", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("allergy_1", StringType(), True),
        StructField("allergy_2", StringType(), True),
        StructField("allergy_3", StringType(), True),
        StructField("description", StringType(), True),
        StructField("disease_1", StringType(), True),
        StructField("disease_2", StringType(), True),
        StructField("disease_3", StringType(), True),
    ])

    # Read the JSON file
    df = spark.read.option("multiline", "true").json("data.json")

    # Parse the "node_report" JSON string into a struct
    df = df.withColumn("node_report_struct", from_json(df["node_report"].cast("string"), schema))

    # Select fields from the struct
    df = df.select("node_report_struct.*")

    # Cache the DataFrame
    df.cache()

    # Write DataFrame to Elasticsearch
    df.write.format("org.elasticsearch.spark.sql") \
        .option("es.nodes", "localhost") \
        .option("es.port", "9200") \
        .option("es.resource", "test") \
        .mode("overwrite") \
        .save()
