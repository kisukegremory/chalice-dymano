from chalice import Chalice, AuthResponse
import json
import boto3




app = Chalice(app_name='token-api-chalice')
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')

@app.authorizer()
def myauth(event):
    if event.token == 'allow':
        return AuthResponse(['*'], principal_id='id')
    return AuthResponse([], principal_id='user')



@app.route('/token',methods=['POST'], authorizer=myauth)
def by_dynamo():
    table = dynamodb.Table('Tokens')
    res = table.get_item(Key={'token': 'madoka'})
    json_obj = res['Item']['data']
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json_obj
    }