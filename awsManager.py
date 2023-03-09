import configparser
import boto3
import requests
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

player_table_name = "players"
qr_table_name = "qrs"

def getResourceAndValidate():
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
        return dynamodb_res

    except:
        print("Welcome to the AWS DynamoDB Shell(D5)")
        print("You are now conneced to your DB storage")
        print("Error: Please review procedures for authenticating your account on AWS DynamoDB")
        quit()

def createPlayerTable():
    global player_table_name
    dynamodb = getResourceAndValidate()
    response = dynamodb.meta.client.list_tables()
    if player_table_name in response['TableNames']:
        print(f'Table {player_table_name} already exists.')
        return 0
    else:

        print("Creating table...")
        table = dynamodb.create_table(
            TableName = player_table_name,
            KeySchema = [
                {
                    'AttributeName': "email",
                    'KeyType': "HASH"
                },
                {
                    'AttributeName': 'name',
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'name',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

    table.meta.client.get_waiter('table_exists').wait(TableName=player_table_name)
    print("Table status:", table.table_status)
    return table


def createQRtable():
    global qr_table_name
    dynamodb = getResourceAndValidate()
    response = dynamodb.meta.client.list_tables()
    if qr_table_name in response['TableNames']:
        print(f'Table {qr_table_name} already exists.')
        return 0
    else:
        print("Creating table...")
        table = dynamodb.create_table(
            TableName = qr_table_name,
            KeySchema = [
                {
                    'AttributeName': "hash_code",
                    'KeyType': "HASH"
                },
                {
                    'AttributeName': 'dateTime',
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'hash_code',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'dateTime',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

    table.meta.client.get_waiter('table_exists').wait(TableName=qr_table_name)
    print("Table status:", table.table_status)
    return table


def getPlayerScores():
    try:
        global player_table_name
        dynamodb = getResourceAndValidate()
        table = dynamodb.Table(player_table_name)
        response = table.scan()

        top_five = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            top_five.extend(response['Items'])

        sorted_players = sorted(top_five, key=lambda x: x['points'], reverse=True)[:5]


        top_five = []
        
        count_players = 0
        for entry in sorted_players:
            if (count_players==5):
                break
            top_five.append(entry)
            count_players = count_players + 1
            
        return top_five
    except Exception as e:
        return e

def insertPlayerItem(points, email, name):
    try:
        global player_table_name
        dynamodb = getResourceAndValidate()
        table = dynamodb.Table(player_table_name)
        # Use the Query operation to check if a player with the specified email exists
        first_response = table.query(
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={
                ':email': email
            }
        )


        if first_response.get('Count', 0) > 0:
            # Add name checking
            old_name = first_response['Items'][0]['name']
            if name != old_name:
                print("Names do not match...")
                print("Switching name to old name...")
                name = old_name
            old_points = first_response['Items'][0]['points']
            print('Player with email', email, 'exists in the table. Adding points...')
            response = table.update_item(
                Key={
                    'email': email,
                    'name': name
                },
                UpdateExpression="SET points = points + :points",
                ExpressionAttributeValues={
                    ":points": points
                },
                ReturnValues="UPDATED_NEW"
            )
        else:
            print("Player does not exsist. Creating player...")
            response = table.put_item(
                Item={
                    'email': email,
                    'name': name,
                    'points': points
                }
            )
        return 0
    except:
        print("Error occurred in insertPlayerItem")
        return -1

def insertHashItem(hash_code):
    global qr_table_name
    dynamodb = getResourceAndValidate()
    table = dynamodb.Table(qr_table_name)

    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d_%H:%M:%S")

    response = table.put_item(
        Item={
            'hash_code': hash_code,
            'dateTime': date_time_str
        }
    )
    return response

def checkHash(hash_id):
    global qr_table_name
    dynamodb = getResourceAndValidate()
    table = dynamodb.Table(qr_table_name)
    first_response = table.query(
        KeyConditionExpression='hash_code = :hash_code',
        ExpressionAttributeValues={
            ':hash_code': hash_id
        }
    )
    if first_response.get('Count', 0) > 0:
        # Found!
        return 0
    else:
        return -1
    
def removeHash(hash_id):
    try:
        global qr_table_name
        dynamodb = getResourceAndValidate()
        table = dynamodb.Table(qr_table_name)
        # Set up primary key of the item you want to delete
        key = table.key_schema[0].get('AttributeName')
        first_response = table.query(
        KeyConditionExpression='hash_code = :hash_code',
        ExpressionAttributeValues={
            ':hash_code': hash_id
        }
        )
        dateTime = first_response['Items'][0]['dateTime']
        primary_key = {'hash_code': hash_id, 'dateTime': dateTime}
        # Delete the item with the matching primary key
        response = table.delete_item(
            Key=primary_key
        )
        return 0
    except Exception as e:
        print("Error occurred in removeHash()")
        print(e)
        return -1