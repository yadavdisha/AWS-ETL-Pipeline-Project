import os
import gzip
import base64
import json
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def process_event(event: dict) -> dict:
    """Process incoming event and categorize it"""
    if "awslogs" in event:
        # CloudWatch Logs event (errors)
        decoded_payload = base64.b64decode(event["awslogs"]["data"])
        uncompressed_payload = gzip.decompress(decoded_payload)
        return {'type': 'error', 'data': json.loads(uncompressed_payload)}
    elif "Records" in event and "s3" in event["Records"][0]:
        # S3 Event (success)
        s3_event = event["Records"][0]["s3"]
        return {
            'type': 'success',
            'data': {
                "bucket": s3_event["bucket"]["name"],
                "key": s3_event["object"]["key"]
            }
        }
    return {'type': 'unknown'}

def prepare_notification_content(event_type: str, payload: dict) -> dict:
    """Prepare notification content based on event type"""
    if event_type == 'success':
        return {
            "subject": f"Success: File processed in {payload['bucket']}",
            "body": f"✅ Successfully wrote to s3://{payload['bucket']}/{payload['key']}"
        }
    
    # Error notification content
    log_events = payload.get('logEvents', [])
    lambda_name = payload.get('logGroup', '/aws/lambda/unknown').split('/')[-1]
    
    return {
        "subject": f"Error: {lambda_name}",
        "body": "\n".join(
            e.get('message', 'No message') 
            for e in log_events
        ),
        "context": {
            "logGroup": payload.get('logGroup', 'N/A'),
            "logStream": payload.get('logStream', 'N/A'),
            "lambdaName": lambda_name
        }
    }

def send_sns_notification(subject: str, message: str, notification_type: str):
    """Send notification to appropriate SNS topic"""
    sns_client = boto3.client('sns')
    
    # Get topic ARN from environment variables
    topic_arn = os.environ.get(
        'SNS_SUCCESS_TOPIC_ARN' if notification_type == 'success' 
        else 'SNS_ERROR_TOPIC_ARN'
    )
    
    if not topic_arn:
        logger.error(f"Missing {notification_type} SNS topic ARN")
        return False

    try:
        sns_client.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
        return True
    except ClientError as e:
        logger.error(f"SNS publish failed: {str(e)}")
        return False

def lambda_handler(event, context):
    """Main Lambda entry point"""
    processed_event = process_event(event)
    
    if processed_event['type'] == 'unknown':
        logger.error("Unrecognized event format")
        return {"statusCode": 400, "body": "Bad Request"}

    # Prepare notification content
    notification = prepare_notification_content(
        processed_event['type'],
        processed_event['data']
    )

    # Send to appropriate SNS topic
    success = send_sns_notification(
        subject=notification['subject'],
        message=notification['body'],
        notification_type=processed_event['type']
    )

    if not success:
        return {"statusCode": 500, "body": "Notification failed"}

    return {"statusCode": 200, "body": "Notification sent"}