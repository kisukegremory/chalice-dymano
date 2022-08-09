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



@app.route('/dynamo',methods=['POST'], authorizer=myauth)
def by_dynamo():
    table = dynamodb.Table('googlesheets')
    res = table.get_item(Key={'token': 'googlesheets'})
    json_obj = res['Item']['json']
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json_obj
    }