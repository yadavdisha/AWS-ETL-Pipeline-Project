import sys
import boto3  # AWS SDK for Python (Boto3)
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Resolve job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize SparkContext, GlueContext, and Job
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data directly from S3 (JSON format)
source_path = "s3://mycodepipelinebucket13/input/hospital.json"
df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",  # Input is in JSON format
    connection_options={"paths": [source_path]},
    format_options={"withHeader": True}
)

# Convert JSON to Parquet using a Lambda function
# Step 1: Invoke the Lambda function
lambda_client = boto3.client('lambda')  # Initialize Lambda client
lambda_response = lambda_client.invoke(
    FunctionName='lambda.py',  # Replace with your Lambda function name
    InvocationType='RequestResponse',  # Synchronous invocation
    Payload=json.dumps({
        'source_bucket': 'mycodepipelinebucket13',
        'source_key': 'input/hospital.json',
        'destination_bucket': 'mycodepipelinebucket13',
        'destination_key': 'output/hospital.parquet'
    })
)

# Step 2: Check Lambda response
if lambda_response['StatusCode'] == 200:
    print("Lambda function executed successfully!")
    # Read the Parquet file created by the Lambda function
    parquet_path = "s3://mycodepipelinebucket13/output/hospital.parquet"
    parquet_df = glueContext.create_dynamic_frame.from_options(
        connection_type="s3",
        format="parquet",  # Input is now in Parquet format
        connection_options={"paths": [parquet_path]}
    )
else:
    raise Exception("Lambda function failed to execute!")

# Write the Parquet data to Redshift
redshift_connection_options = {
    "url": "jdbc:redshift://your-cluster-name:port/database-name",
    "user": "your-username",
    "password": "your-password",
    "dbtable": "your-redshift-table",  # Destination table name in Redshift
    "redshiftTmpDir": "s3://your-temporary-dir-for-redshift/",  # Temporary directory for Redshift data loading
    "aws_iam_role": "arn:aws:iam::your-account-id:role/your-iam-role"  # IAM role with Redshift access
}

glueContext.write_dynamic_frame.from_options(
    frame=parquet_df,  # Use the Parquet DataFrame
    connection_type="redshift",
    connection_options=redshift_connection_options
)

# Commit the job
job.commit()
