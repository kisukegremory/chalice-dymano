
import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
table = dynamodb.Table(name='TestTable')

def create_table(dynamodb):
    table = dynamodb.create_table(
        TableName = 'TestTable',
        KeySchema = [
            {
                'AttributeName':'token',
                'KeyType':'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName':'token',
                'AttributeType':'S'
            },
        ],
        BillingMode = 'PAY_PER_REQUEST'
    )
    return table

def upload_credentials(table, token: str):
    with open('credentials.json') as creds:
        data = json.load(creds)

    table.put_item(
        Item={
            'token':token,
            'data':data
        }
    )