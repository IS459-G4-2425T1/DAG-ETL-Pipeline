
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, avg, when, floor, trim, concat, lit, desc, lag, sum, to_date, concat_ws, date_format
from pyspark.sql import functions as F
from awsglue.dynamicframe import DynamicFrame

# Initialize a Spark context
spark_context = SparkContext.getOrCreate()

# Initialize a Glue context
glue_context = GlueContext(spark_context)

# Specify the S3 path to your Parquet file
parquet_path = "s3://airtime-historical-data/clean/pipeline-1/"

# Read the Parquet file into a Spark DataFrame
df = glue_context.spark_session.read.parquet(parquet_path)

# Show the first few rows of the DataFrame to verify it's loaded correctly
df.show()

df = df.withColumn(
    "Season",
    F.when((df["month"] == 12) | (df["month"] == 1) | (df["month"] == 2), "Winter")
     .when((df["month"] >= 3) & (df["month"] <= 5), "Spring")
     .when((df["month"] >= 6) & (df["month"] <= 8), "Summer")
     .when((df["month"] >= 9) & (df["month"] <= 11), "Fall")
)

# Show the DataFrame to verify the new column
df.show()

# Create a new column 'Total delay' by adding 'depdelay' and 'arrdelay'
df = df.withColumn("totaldelay", F.col("depdelay") + F.col("arrdelay"))

# Show the updated DataFrame to verify the new column
df.show()
df = df.withColumn(
    "Severity",
    F.when(df["totaldelay"] < 60, "Minimal")
     .when((df["totaldelay"] >= 60) & (df["totaldelay"] < 120), "Moderate")
     .when((df["totaldelay"] >= 120) & (df["totaldelay"] < 180), "Major")
     .when((df["totaldelay"] >= 180) & (df["totaldelay"] <= 360), "Significant")
     .when(df["totaldelay"] > 360, "Severe")
     .otherwise("No Delay")
)

# Show the DataFrame to verify the new column
df.show()
s3 = "s3://pipeline1-data-storage/processed-data/"
df.write.mode("overwrite").parquet(s3 + "df/")
job.commit()