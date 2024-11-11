import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame
import re

def sparkUnion(glueContext, unionType, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql("(select * from source1) UNION " + unionType + " (select * from source2)")
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Additional data
Additionaldata_node1731058998685 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://airline-additional-data/historical_2024_data.csv"], "recurse": True}, transformation_ctx="Additionaldata_node1731058998685")

# Script generated for node Historic data
Historicdata_node1731058769961 = glueContext.create_dynamic_frame.from_catalog(database="airline-historical-crawled", table_name="airline_csv_shuffle", transformation_ctx="Historicdata_node1731058769961")

# Script generated for node Additional schema change
Additionalschemachange_node1731059043356 = ApplyMapping.apply(frame=Additionaldata_node1731058998685, mappings=[("ArrDelay", "string", "arrdelay", "int"), ("CarrierDelay", "string", "carrierdelay", "int"), ("DayOfWeek", "string", "dayofweek", "int"), ("DayofMonth", "string", "dayofmonth", "int"), ("DepDelay", "string", "depdelay", "int"), ("DepTime", "string", "deptime", "int"), ("Dest", "string", "dest", "string"), ("LateAircraftDelay", "string", "lateaircraftdelay", "int"), ("Month", "string", "month", "int"), ("NASDelay", "string", "nasdelay", "int"), ("Origin", "string", "origin", "string"), ("SecurityDelay", "string", "securitydelay", "int"), ("WeatherDelay", "string", "weatherdelay", "int"), ("Year", "string", "year", "int")], transformation_ctx="Additionalschemachange_node1731059043356")

# Script generated for node Historic schema change
Historicschemachange_node1731058836035 = ApplyMapping.apply(frame=Historicdata_node1731058769961, mappings=[("arrdelay", "int", "arrdelay", "int"), ("carrierdelay", "int", "carrierdelay", "int"), ("dayofweek", "int", "dayofweek", "int"), ("dayofmonth", "int", "dayofmonth", "int"), ("depdelay", "int", "depdelay", "int"), ("deptime", "int", "deptime", "int"), ("dest", "string", "dest", "string"), ("lateaircraftdelay", "int", "lateaircraftdelay", "int"), ("month", "int", "month", "int"), ("nasdelay", "int", "nasdelay", "int"), ("origin", "string", "origin", "string"), ("securitydelay", "int", "securitydelay", "int"), ("weatherdelay", "int", "weatherdelay", "int"), ("year", "int", "year", "int")], transformation_ctx="Historicschemachange_node1731058836035")

# Script generated for node Union
Union_node1731166969132 = sparkUnion(glueContext, unionType = "ALL", mapping = {"source1": Additionalschemachange_node1731059043356, "source2": Historicschemachange_node1731058836035}, transformation_ctx = "Union_node1731166969132")

# Script generated for node Change Schema
ChangeSchema_node1731080630378 = ApplyMapping.apply(frame=Union_node1731166969132, mappings=[("arrdelay", "int", "arrdelay", "int"), ("carrierdelay", "int", "carrierdelay", "int"), ("dayofweek", "int", "dayofweek", "int"), ("dayofmonth", "int", "dayofmonth", "int"), ("depdelay", "int", "depdelay", "int"), ("deptime", "int", "deptime", "int"), ("dest", "string", "dest", "string"), ("lateaircraftdelay", "int", "lateaircraftdelay", "int"), ("month", "int", "month", "int"), ("nasdelay", "int", "nasdelay", "int"), ("origin", "string", "origin", "string"), ("securitydelay", "int", "securitydelay", "int"), ("weatherdelay", "int", "weatherdelay", "int"), ("year", "int", "year", "int")], transformation_ctx="ChangeSchema_node1731080630378")

# Script generated for node Filter
Filter_node1731079073857 = Filter.apply(frame=ChangeSchema_node1731080630378, f=lambda row: (not(row["arrdelay"] == 0) and not(row["depdelay"] == 0) and bool(re.match("^(?!NA$).*", row["dest"])) and bool(re.match("^(?!NA$).*", row["origin"]))), transformation_ctx="Filter_node1731079073857")

# Script generated for node Amazon S3
AmazonS3_node1731059334655 = glueContext.write_dynamic_frame.from_options(frame=Filter_node1731079073857, connection_type="s3", format="glueparquet", connection_options={"path": "s3://airtime-historical-data/clean/pipeline-1/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1731059334655")

job.commit()