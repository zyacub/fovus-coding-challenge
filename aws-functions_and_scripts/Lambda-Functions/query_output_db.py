import json
import boto3
import urllib.parse


client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fovusOutputDB')

def lambda_handler(event, context):
    # TODO implement
    try:
        body = {}
        
        body = table.scan()
        body = body["Items"]
        print("ITEMS----")
        print(body)
        responseBody = []
        for items in body:
            responseItems = [
                {"id": items['id'], 'path': items['output_file_path']}]
            responseBody.append(responseItems)
        body = responseBody
        return {
            'statusCode': 200,
            'body': json.dumps(body)
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
