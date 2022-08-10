
import click
import boto3
import json
import os
from time import sleep

TABLE_NAME = os.environ['table_name']


def create_table(dynamodb):
    table = dynamodb.create_table(
        TableName = TABLE_NAME,
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
    sleep(7)
    return table

def check_table_existence(dynamodb) -> bool:
    tables = list(dynamodb.tables.all())
    verified_tables = list(filter(lambda x: x.name == TABLE_NAME,tables))
    return bool(verified_tables)

def upload_credentials(table, path: str, token: str):
    with open(path) as creds:
        data = json.load(creds)

    table.put_item(
        Item={
            'token':token,
            'data':data
        }
    )

    print("Successfully updated token")


@click.command()
@click.option('--file', '-f', 'file', required=True, help='path of the json file')
@click.option('--token', '-t', 'token', required=True, help='token name')
def main(file: str, token: str):
    dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
    if check_table_existence(dynamodb):
        table = dynamodb.Table(name='Tokens')
    else:
        table = create_table(dynamodb)

    print(table)

    upload_credentials(table, file, token)


if __name__ == '__main__':
    main()