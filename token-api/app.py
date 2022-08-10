from chalice import Chalice, AuthResponse
import boto3
import os

app = Chalice(app_name='token-api-chalice')
dynamodb = boto3.resource('dynamodb')

@app.authorizer()
def myauth(event):
    if event.token == os.environ['api-key']:
        return AuthResponse(['*'], principal_id='id')
    return AuthResponse([], principal_id='user')


@app.route('/token',methods=['POST'], authorizer=myauth)
def by_dynamo():
    table = dynamodb.Table(os.environ['table_name'])
    res = table.get_item(Key={'token': os.environ['token_name']})
    json_obj = res['Item']['data']
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json_obj
    }