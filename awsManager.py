import configparser
import os
import sys
import pathlib
import boto3
import requests
import pandas as pd
import asyncio
import time

def createTable(name):

    config = configparser.ConfigParser()
    config.read("dynamoDB.conf")
    aws_access_key_id = config['default']['aws_access_key_id']
    aws_secret_access_key = config['default']['aws_secret_access_key']

    #Try making a connection to S3 using boto3
    try:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        dynamodb_res = boto3.resource('dynamodb', region_name='ca-central-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        dynamodb = boto3.client('dynamodb', region_name='ca-central-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        print("Welcome to the AWS DynamoDB Shell(D5)")
        print("You are now conneced to your DB storage")

    except:
        print("Welcome to the AWS DynamoDB Shell(D5)")
        print("You are now conneced to your DB storage")
        print("Error: Please review procedures for authenticating your account on AWS DynamoDB")
        quit()

    # Check if the table already exists
    try:
        table = dynamodb.Table(name)

    # If the table does not exist, create it
    except:
        table = dynamodb.create_table(
            TableName = name,
            KeySchema = [
                {
                    'AttributeName': "email",
                    'KeyType': "HASH"
                },
                {
                    'AttributeName': "name",
                    'KeyType': "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': "email",
                    'AttributeType': "S"
                },
                {
                    'AttributeName': "name",
                    'AttributeType': "S"
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

    table.meta.client.get_waiter('table_exists').wait(TableName=name)
    print("Table status:", table.table_status)
    return table


def insertItem(dynamo, table, points, email, name):

    #Check if the player already exists
    response = dynamo.batch_get_item(
        RequestItems={
            'my-table': {
                'Keys': [
                    {
                        'id': email
                    },
                    {
                        'id': name
                    },
                ],
                'ConsistentRead': True
            }
        },
        ReturnConsumedCapacity='TOTAL'
    )

    if not response:
        response = table.put_item(
            Item={
                'email': email,
                'name': name,
                'points': points
            }
        )
    else:
        table.update_item (
            Key={
                'email': email
            },
            UpdateExpression=f'SET points = :{response.points + points}",
            ExpressionAttributeValues={
                ':newCountry': "Canada"
            },
            ReturnValues="UPDATED_NEW"
        )


    return response