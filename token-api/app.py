from chalice import Chalice
import json
import boto3

app = Chalice(app_name='token-api-chalice')
s3 = boto3.client('s3')

@app.route('/')
def index():
    bucket = 's3-test-googlesheets'
    key = 'credentials.json'
    
    res = s3.get_object(Bucket=bucket, Key=key)
    print(res)
    content = res['Body']
    
    json_obj = json.loads(content.read())
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(json_obj)
    }