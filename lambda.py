import boto3
import json
import uuid
from datetime import datetime

# Initialize clients
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('images-labels-table')  # Replace with your DynamoDB table name

def lambda_handler(event, context):
    # Get the S3 bucket and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Call Amazon Rekognition to detect labels
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_key
            }
        },
        MaxLabels=10,  # Adjust as needed
        MinConfidence=70  # Adjust confidence threshold
    )
    
    # Extract labels
    labels = [label['Name'] for label in response['Labels']]
    
    # Save data to DynamoDB
    image_id = str(uuid.uuid4())  # Generate a unique ID for the image
    timestamp = datetime.utcnow().isoformat()
    
    table.put_item(
        Item={
            'ImageID': image_id,
            'S3Bucket': bucket_name,
            'S3Key': object_key,
            'Labels': labels,
            'Timestamp': timestamp
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Labels detected and saved to DynamoDB!')
    }