import json
import boto3
import urllib.parse

from boto3.dynamodb.conditions import Key

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fovusInputDB')

def lambda_handler(event, context):
    # TODO implement
    
    print("starting function")
    try:
        # Parse query string parameters
        params = event.get('queryStringParameters', {})
        input_file_path = params.get('filepath', '')
        input_text = params.get('textInput', '')
        id = params.get('id', '')
        
        # URL decode the filename 
        input_file_path = urllib.parse.unquote_plus(input_file_path)
        
        response = table.put_item(
            Item={
                'id': id,
                'input_text': input_text,
                'input_file_path': input_file_path
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,GET',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps({'message': 'Data saved successfully', 'id': id})
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

