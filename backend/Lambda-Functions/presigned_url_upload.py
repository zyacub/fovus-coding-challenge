import json
import boto3
import urllib.parse

# Initializing s3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    # Parse query string parameters
    params = event.get('queryStringParameters', {})
    filename = params.get('filename', '')
    text_input = params.get('textInput', '')
    
    # URL decode the filename 
    filename = urllib.parse.unquote_plus(filename)
    
    # Ensure filename is not empty
    if not filename:
        return {
            'statusCode': 400,
            'body': json.dumps('Filename is required')
        }
    
    bucket_name = 'fovus-coding-aws'
    
    key = f'{filename}'
    
    metadata = {
        'textInput': text_input
    }
    
    presigned_url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': bucket_name,
            'Key': key,
            'ContentType': 'application/input',  # Use a generic content type
            'Metadata': metadata
        },
        ExpiresIn=3600,
        HttpMethod='PUT'
    )
    
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET'
        },
        'body': json.dumps({
            'presignedUrl': presigned_url,
            'key': key
        })
    }
    return response