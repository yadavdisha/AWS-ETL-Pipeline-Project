import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data directly from S3
source_path = "s3://mycodepipelinebucket13/input/product_data.csv"
df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="csv",
    connection_options={"paths": [source_path]},
    format_options={"withHeader": True}
)



# Convert to JSON format
json_path = "s3://mycodepipelinebucket13/output/target-data.json"
glueContext.write_dynamic_frame.from_options(
    frame=df,
    connection_type="s3",
    connection_options={"path": json_path},
    format="json"
)

job.commit()
