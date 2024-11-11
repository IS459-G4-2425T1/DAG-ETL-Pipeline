import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
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

# Script generated for node Active airlines
Activeairlines_node1731077522274 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://active-carriers-data/active_carriers.csv"], "recurse": True}, transformation_ctx="Activeairlines_node1731077522274")

# Script generated for node Additional Schema
AdditionalSchema_node1731218527877 = ApplyMapping.apply(frame=Additionaldata_node1731058998685, mappings=[("arrdelay", "string", "arrdelay", "int"), ("arrtime", "string", "arrtime", "int"), ("crsarrtime", "string", "crsarrtime", "int"), ("crsdeptime", "string", "crsdeptime", "int"), ("crselapsedtime", "string", "crselapsedtime", "int"), ("dayofweek", "string", "dayofweek", "int"), ("dayofmonth", "string", "dayofmonth", "int"), ("depdelay", "string", "depdelay", "int"), ("deptime", "string", "deptime", "int"), ("dest", "string", "dest", "string"), ("flightnum", "string", "flightnum", "string"), ("month", "string", "month", "int"), ("origin", "string", "origin", "string"), ("tailnum", "string", "tailnum", "string"), ("uniquecarrier", "string", "uniquecarrier", "string"), ("year", "string", "year", "int")], transformation_ctx="AdditionalSchema_node1731218527877")

# Script generated for node Historic schema change
Historicschemachange_node1731058836035 = ApplyMapping.apply(frame=Historicdata_node1731058769961, mappings=[("arrdelay", "int", "arrdelay", "int"), ("arrtime", "int", "arrtime", "int"), ("crsarrtime", "int", "crsarrtime", "int"), ("crsdeptime", "int", "crsdeptime", "int"), ("crselapsedtime", "int", "crselapsedtime", "int"), ("dayofweek", "int", "dayofweek", "int"), ("dayofmonth", "int", "dayofmonth", "int"), ("depdelay", "int", "depdelay", "int"), ("deptime", "int", "deptime", "int"), ("dest", "string", "dest", "string"), ("flightnum", "int", "flightnum", "string"), ("month", "int", "month", "int"), ("origin", "string", "origin", "string"), ("tailnum", "string", "tailnum", "string"), ("uniquecarrier", "string", "uniquecarrier", "string"), ("year", "int", "year", "int")], transformation_ctx="Historicschemachange_node1731058836035")

# Script generated for node Union
Union_node1731125711325 = sparkUnion(glueContext, unionType = "ALL", mapping = {"source1": AdditionalSchema_node1731218527877, "source2": Historicschemachange_node1731058836035}, transformation_ctx = "Union_node1731125711325")

# Script generated for node Check Schema
CheckSchema_node1731083196440 = ApplyMapping.apply(frame=Union_node1731125711325, mappings=[("arrdelay", "int", "arrdelay", "int"), ("arrtime", "int", "arrtime", "int"), ("crsarrtime", "int", "crsarrtime", "int"), ("crsdeptime", "int", "crsdeptime", "int"), ("crselapsedtime", "int", "crselapsedtime", "int"), ("dayofweek", "int", "dayofweek", "int"), ("dayofmonth", "int", "dayofmonth", "int"), ("depdelay", "int", "depdelay", "int"), ("deptime", "int", "deptime", "int"), ("dest", "string", "dest", "string"), ("flightnum", "string", "flightnum", "string"), ("month", "int", "month", "int"), ("origin", "string", "origin", "string"), ("tailnum", "string", "tailnum", "string"), ("uniquecarrier", "string", "uniquecarrier", "string"), ("year", "int", "year", "int")], transformation_ctx="CheckSchema_node1731083196440")

# Script generated for node Join
CheckSchema_node1731083196440DF = CheckSchema_node1731083196440.toDF()
Activeairlines_node1731077522274DF = Activeairlines_node1731077522274.toDF()
Join_node1731078421278 = DynamicFrame.fromDF(CheckSchema_node1731083196440DF.join(Activeairlines_node1731077522274DF, (CheckSchema_node1731083196440DF['uniquecarrier'] == Activeairlines_node1731077522274DF['Airline Code']), "leftsemi"), glueContext, "Join_node1731078421278")

# Script generated for node Change Schema
ChangeSchema_node1731078611156 = ApplyMapping.apply(frame=Join_node1731078421278, mappings=[("arrdelay", "int", "arrdelay", "int"), ("arrtime", "int", "arrtime", "int"), ("crsarrtime", "int", "crsarrtime", "int"), ("crsdeptime", "int", "crsdeptime", "int"), ("crselapsedtime", "int", "crselapsedtime", "int"), ("dayofweek", "int", "dayofweek", "int"), ("dayofmonth", "int", "dayofmonth", "int"), ("depdelay", "int", "depdelay", "int"), ("deptime", "int", "deptime", "int"), ("dest", "string", "dest", "string"), ("flightnum", "string", "flightnum", "string"), ("month", "int", "month", "int"), ("origin", "string", "origin", "string"), ("tailnum", "string", "tailnum", "string"), ("uniquecarrier", "string", "uniquecarrier", "string"), ("year", "int", "year", "int")], transformation_ctx="ChangeSchema_node1731078611156")

# Script generated for node Filter
Filter_node1731079073857 = Filter.apply(frame=ChangeSchema_node1731078611156, f=lambda row: (not(row["arrdelay"] == 0) and not(row["depdelay"] == 0) and bool(re.match("^(?!NA$).*", row["dest"])) and bool(re.match("^(?!NA$).*", row["origin"])) and bool(re.match("^(?!NA$).*", row["flightnum"])) and bool(re.match("^(?!NA$).*", row["tailnum"])) and bool(re.match("^(?!NA$).*", row["uniquecarrier"]))), transformation_ctx="Filter_node1731079073857")

# Script generated for node Amazon S3
AmazonS3_node1731059334655 = glueContext.write_dynamic_frame.from_options(frame=Filter_node1731079073857, connection_type="s3", format="glueparquet", connection_options={"path": "s3://airtime-historical-data/clean/pipeline-2/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1731059334655")

job.commit()