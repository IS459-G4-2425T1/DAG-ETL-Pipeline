import sys
from datetime import datetime
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, regexp_replace, lit, when
from pyspark.sql.types import IntegerType, StringType, StructType, StructField

# Initialize Glue and Spark contexts
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# S3 path to the .csv.shuffle file
s3_input_path = "s3://airtime-historical-data/read/airline.csv.shuffle"

# Define an explicit schema based on Glue Catalog
schema = StructType([
    StructField("ActualElapsedTime", StringType(), True),
    StructField("AirTime", StringType(), True),
    StructField("ArrDelay", StringType(), True),
    StructField("ArrTime", StringType(), True),
    StructField("CRSArrTime", StringType(), True),
    StructField("CRSDepTime", StringType(), True),
    StructField("CRSElapsedTime", StringType(), True),
    StructField("CancellationCode", StringType(), True),
    StructField("Cancelled", StringType(), True),
    StructField("CarrierDelay", StringType(), True),
    StructField("DayOfWeek", StringType(), True),
    StructField("DayofMonth", StringType(), True),
    StructField("DepDelay", StringType(), True),
    StructField("DepTime", StringType(), True),
    StructField("Dest", StringType(), True),
    StructField("Distance", StringType(), True),
    StructField("Diverted", StringType(), True),
    StructField("FlightNum", StringType(), True),
    StructField("LateAircraftDelay", StringType(), True),
    StructField("Month", StringType(), True),
    StructField("NASDelay", StringType(), True),
    StructField("Origin", StringType(), True),
    StructField("SecurityDelay", StringType(), True),
    StructField("TailNum", StringType(), True),
    StructField("TaxiIn", StringType(), True),
    StructField("TaxiOut", StringType(), True),
    StructField("UniqueCarrier", StringType(), True),
    StructField("WeatherDelay", StringType(), True),
    StructField("Year", StringType(), True)
])

# Read the file into a Spark DataFrame with the defined schema
df = spark.read.format("csv") \
    .option("header", "true") \
    .schema(schema) \
    .load(s3_input_path)

# Data Cleansing: Handle missing and malformed data
clean_df = df \
    .withColumn("ActualElapsedTime", regexp_replace(col("ActualElapsedTime"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("AirTime", regexp_replace(col("AirTime"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("ArrDelay", regexp_replace(col("ArrDelay"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("DepDelay", regexp_replace(col("DepDelay"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("ArrTime", regexp_replace(col("ArrTime"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("DepTime", regexp_replace(col("DepTime"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("CRSArrTime", regexp_replace(col("CRSArrTime"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("CRSDepTime", regexp_replace(col("CRSDepTime"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("CRSElapsedTime", regexp_replace(col("CRSElapsedTime"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("Cancelled", when(col("Cancelled") == "", None).otherwise(col("Cancelled").cast(IntegerType()))) \
    .withColumn("CarrierDelay", regexp_replace(col("CarrierDelay"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("DayOfWeek", regexp_replace(col("DayOfWeek"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("DayofMonth", regexp_replace(col("DayofMonth"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("Diverted", regexp_replace(col("Diverted"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("FlightNum", regexp_replace(col("FlightNum"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("LateAircraftDelay", regexp_replace(col("LateAircraftDelay"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("Month", regexp_replace(col("Month"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("NASDelay", regexp_replace(col("NASDelay"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("SecurityDelay", regexp_replace(col("SecurityDelay"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("TaxiIn", regexp_replace(col("TaxiIn"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("TaxiOut", regexp_replace(col("TaxiOut"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("WeatherDelay", regexp_replace(col("WeatherDelay"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("Year", regexp_replace(col("Year"), "[^0-9]", "").cast(IntegerType())) \
    .withColumn("UniqueCarrier", when(col("UniqueCarrier") == "", None).otherwise(col("UniqueCarrier"))) \
    .withColumn("Origin", when(col("Origin") == "", None).otherwise(col("Origin"))) \
    .withColumn("Dest", when(col("Dest") == "", None).otherwise(col("Dest"))) \
    .withColumn("TailNum", when(col("TailNum") == "", None).otherwise(col("TailNum"))) \
    .withColumn("CancellationCode", when(col("CancellationCode") == "", None).otherwise(col("CancellationCode")))

# Convert Spark DataFrame to Glue DynamicFrame
dynamic_df = DynamicFrame.fromDF(clean_df, glueContext, "dynamic_df")

# Print the schema for verification
dynamic_df.printSchema()

# Convert DynamicFrame to DataFrame to add the 'partition_0' column
df_with_partition = dynamic_df.toDF().withColumn("partition_0", col("Year").cast(StringType()))

# Convert back to DynamicFrame
dynamic_df_with_partition = DynamicFrame.fromDF(df_with_partition, glueContext, "dynamic_df_with_partition")

output_path = f"s3://airtime-historical-data/write/airline.csv.shuffle"

# Save the processed data to the S3 location in Parquet format
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_df_with_partition,
    connection_type="s3",
    connection_options={"path": output_path, "partitionKeys": ["partition_0"], "mode": "overwrite"},
    format="parquet",
    format_options={"compression": "snappy"}  # Optional: Specify compression
)
