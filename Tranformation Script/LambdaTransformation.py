import os
import awswrangler as wr  # AWS Wrangler for Athena, S3, and Glue interactions
import logging
import boto3
import pandas as pd

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Execution started")
    
    try:
        logger.info("Raw event: %s", event)
        
        # Validate S3 event structure
        if 'Records' not in event or not event['Records']:
            logger.error(" Invalid S3 event: No Records found.")
            return {"statusCode": 400, "message": "Invalid S3 event"}
        
        record = event['Records'][0]
        if 's3' not in record:
            logger.error(" Missing S3 key in event payload.")
            return {"statusCode": 400, "message": "Invalid S3 event"}
        
        #  Extract bucket and file details
        bucket = "hospital-de-raw-data-dev"  # Correct bucket name
        key = "hospital/raw_data/healthcare_sample.json"  # Correct S3 key
        input_path = f"s3://{bucket}/{key}"
        logger.info(f" Processing file: {input_path}")

        # Read JSON data from S3
        try:
            logger.info(f" Reading JSON data from {input_path}")
            df = wr.s3.read_json(path=input_path)
            logger.info(f"Data loaded: {len(df)} rows from {input_path}")
        except Exception as e:
            logger.error(f" Failed to read JSON file: {str(e)}")
            return {"statusCode": 500, "message": f"Failed to read JSON file: {str(e)}"}

        # Validate data before writing
        if df.empty:
            logger.warning("" No data to process. Skipping write operation.")
            return {"statusCode": 200, "message": "No data available"}
            
        # dd partition column (for better query performance)
        df['processing_date'] = pd.to_datetime('today').date()
        
        #  Write to S3 as Parquet with partitioning
        try:
            logger.info(" Writing data to S3 as Parquet...")
            wr.s3.to_parquet(
                df=df,
                path=os.environ['s3_cleansed_layer'],  # Ensure you have this environment variable set
                dataset=True,
                database=os.environ['glue_catalog_db_name'],  # Ensure you have this environment variable set
                table=os.environ['glue_catalog_table_name'],  # Ensure you have this environment variable set
                mode=os.environ['write_data_operation'],  # Ensure you have this environment variable set
                compression="snappy",
                partition_cols=['processing_date'],  # Partitioning enabled
                concurrent_partitioning=True,
                schema_evolution=True
            )
            logger.info(f" Successfully wrote to {os.environ['s3_cleansed_layer']}")
        except Exception as e:
            logger.error(f"Failed to write to S3: {str(e)}")
            return {"statusCode": 500, "message": f"Failed to write to S3: {str(e)}"}

        return {"statusCode": 200, "message": " Processing completed successfully"}
        
    except Exception as e:
        logger.error(f" Critical failure: {str(e)}", exc_info=True)
        return {"statusCode": 500, "message": "Lambda execution failed"}
