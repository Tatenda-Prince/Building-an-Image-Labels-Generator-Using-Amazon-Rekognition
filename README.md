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


![image_alt]()


3.Now that our bucket is successfully created see example, leave the bucket empty for do upload anything.

![image_alt]()









