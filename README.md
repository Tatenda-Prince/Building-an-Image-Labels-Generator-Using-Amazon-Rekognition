# Building-an-Image-Labels-Generator-Using-Amazon-Rekognition

"Machine Learning"

# Technical Architecture

![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/28fa0a7836cf0c3999a262170b93b16a1d23efae/img/Screenshot%202025-01-29%20155138.png)

## Project Overview

This project automates image analysis using AWS services. Users upload images to an S3 bucket, which triggers an AWS Lambda function. The function sends the image to Amazon Rekognition for analysis, such as object detection, facial recognition, or text extraction. The results are then stored in Amazon DynamoDB for easy access and retrieval.

## Project Objectives

1.Amazon S3: Stores the uploaded images.

2.Amazon Rekognition: Detects labels (objects, scenes, etc.) in the images.

3.AWS Lambda: Processes the image when uploaded to S3, calls Rekognition, and saves the results to DynamoDB.

4.DynamoDB: Stores the image metadata and detected labels.


## Prerequisites

1.AWS Account: Create an AWS Account

2.AWS CLI Installed and Configured: Install & configure AWS CLI to programatically interact with AWS

## Technologies

1.Amazon S3

2.AWS Lambda

3.Amazon Rekognition

4.DynamoDB

## Use case

You work at a company that deals with videos and films and you are tasked with detecting labels to improve searchability.


## Step 1: Set up Amazon S3 Bucket


1.Open your AWS Management Console and navigate to the home console, search for "Amazon S3" click the orange button to create your bucket.


2.Name your bucket and it must globally unique and scroll down leave everything as default until you see the create button and click to create.


![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/76433e4f169bc2a1a96aaa31346eab88bfb02d21/img/Screenshot%202025-01-29%20160819.png)


3.Now that our bucket is successfully created see example, leave the bucket empty for now don't upload anything.

![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/3a852b293767898e2cc5c3efd74cc738a299eb2b/img/Screenshot%202025-01-29%20160847.png)


## Step 2: Set up DynamoDB Table

1.Navigate to the home console, search for "DynanoDB" click the orange button to create table.

2.Name your table and scroll down leave everything as default until you see the create button and click to create.

Primary Key enter: `ImageId` (string) Unique identifier for each image

![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/454c5c88faf959ffca879c83b97a2bbac9f166b5/img/Screenshot%202025-01-29%20161003.png)



3.If your table has status 'ACTIVE' which means it was successfully created see example-

![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/e6d9b22e7b67a493651dc278c7df3527600f482e/img/Screenshot%202025-01-29%20161032.png)


## Step 3: Create a Role for our Lambda 

1.Navigate to "IAM" home console search Roles on your left hand side click on it and you will see a orange button that says create role 

2.AWS Services choose Lambda

![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/76c8b7d942e950acfd5c01af038cd2afb7d9c2e3/img/Screenshot%202025-01-29%20161335.png)


3.On Policies we are to choose three policies

Amazon S3:`s3:GetObject`

Amazon Rekognition: `rekognition:DetectLabels`

DynamoDB: dynamodb:`PutItem`


![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/43bb627807bcae1d2f40c9856c3e21e92056f30d/img/Screenshot%202025-01-29%20161511.png)



4.Give your Role a name see example- then click create Role 


![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/21b8902789adcf5e8cf45194ad0e227ac1644a80/img/Screenshot%202025-01-29%20161600.png)


## Step 4: Create a lambda Lambda Function

1.Search for Lambda click on the orange buttun to create a function see example below-

2.Choose Start  Author from Scratch and give your lambda function a name

![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/4f36ea9e52f85dbcb287c9575cae503ea8d5366f/img/Screenshot%202025-01-29%20161707.png)


3.Now add Permissions choose the existing role that we have created ealier see example below-


![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/56967e641aba26d0d21a2535db3ea6e423aad9ff/img/Screenshot%202025-01-29%20161726.png)


click create


![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/e5defd2842aac3d87e82186a538d998071ad5410/img/Screenshot%202025-01-29%20162003.png)



4.Now that our lambda function was successfully created copy the code below and paste it on the lambda code block and click deploy.

```python
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

```


## code explanation


This AWS Lambda function automatically processes images uploaded to an S3 bucket by detecting labels using Amazon Rekognition and storing the results in a DynamoDB table. When an image is uploaded, the function retrieves the S3 bucket and object key from the event, calls Rekognition to analyze the image, and extracts up to 10 labels with at least 70% confidence.

It then generates a unique ImageID, records a timestamp, and saves the image metadata (bucket name, object key, detected labels, and timestamp) in the DynamoDB table. Finally, it returns a success response indicating that the labels have been detected and stored.


## Step 5: Configure S3 Event Notification

1.Now lets head back to our S3 Bucket the we created ealier under "Properties" to create a event notification that will trigger lambda when we upload a image


2.Scroll dowm until you see the event notification block and then click create event 


![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/8ace6cb74cc11962b365addc4713df4dbe5ccf0e/img/Screenshot%202025-01-29%20162209.png)


3.Enter yor event name and leave everything as default


![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/646f121dc1552983d8f416016d1794d18979d369/img/Screenshot%202025-01-29%20162255.png)


4.On Event type click the block that says ALL OBJECT create events 


![image_alt](https://github.com/Tatenda-Prince/Building-an-Image-Labels-Generator-Using-Amazon-Rekognition/blob/be4e9006a6bbf3d564a1534baf7e0e2526ef3f13/img/Screenshot%202025-01-29%20162310.png)


5.On destination choose Lambda and choose the lambda function we created before see example-


![image_alt]()


6.Now head back to your lambda function and if the event trigger was successfully added.


![image_alt]()





























