import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize SparkContext, GlueContext, and Job
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data directly from S3
source_path = "s3://mycodepipelinebucket13/input/hospital.json"
df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",  # Assuming the input is in JSON format
    connection_options={"paths": [source_path]},
    format_options={"withHeader": True}
)

# Clean the data (if any transformation is required)
# Example: Perform some transformations if necessary

redshift_connection_options = {
    "url": "jdbc:redshift://your-cluster-name:port/database-name",
    "user": "your-username",
    "password": "your-password",
    "dbtable": "your-redshift-table",  # Destination table name in Redshift
    "redshiftTmpDir": "s3://your-temporary-dir-for-redshift/",  # Temporary directory for Redshift data loading
    "aws_iam_role": "arn:aws:iam::your-account-id:role/your-iam-role"  # IAM role with Redshift access
}

# Write the data to Redshift
glueContext.write_dynamic_frame.from_options(
    frame=df,
    connection_type="redshift",
    connection_options=redshift_connection_options
)

# Commit the job
job.commit()
