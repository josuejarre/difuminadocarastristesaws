#!/usr/bin/python3

import os
import boto3

from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

# Get env variables
accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
bucket = os.environ.get('BUCKET_SOURCE')
region = os.environ.get('REGION')

# Create the service Rekognition and assign credentials
rekognition_client = boto3.Session(
    aws_access_key_id=accessKeyId,
    aws_secret_access_key=secretKey,
    region_name=region).client('rekognition')

def looking_faces(keys):
    # Assign parameters and call the service
    try:
        response = rekognition_client.compare_faces(
    SourceImage={
        'S3Object': {
            'Bucket': bucket,
            'Name': keys[0]
        }
    },
    TargetImage={
        'S3Object': {
            'Bucket': bucket,
            'Name': keys[1]
        }
    },
    SimilarityThreshold=90
    )

    except:
        raise Exception("Un error inexperado ha ocurrido al intentar comparar las imagenes")

    return response
