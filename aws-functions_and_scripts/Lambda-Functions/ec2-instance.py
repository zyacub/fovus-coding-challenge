
import boto3

def lambda_handler(event, context):
    record = event['Records'][0]
    
    print(record)
    
    
    # The 'NewImage' contains the new state of the item after the change
    new_image = record['dynamodb']['NewImage']
    id = new_image['id']['S']  # 'S' for String type

    print(f"New item added with ID: {id}")
    
    script = f"""#!/bin/bash
    echo "Performing tasks..."
    sudo yum install -y python
    ID="{id}"
    # Get instance ID
    INSTANCE_ID=$(ec2-metadata -i | cut -d " " -f 2)
    
    # Get file path and input text from ID
    RESULT=$(aws dynamodb get-item \\
    --table-name fovusInputDB \\
    --key '{{"id": {{"S": "'$ID'"}}}}')
    
    FILE_PATH=$(echo $RESULT | jq -r '.Item.input_file_path.S')
    TEXT_VALUE=$(echo $RESULT | jq -r '.Item.input_text.S')
    
    # Create a file with some content
    echo "Task completed at $(date). Item ID: $ID. File Path: $FILE_PATH. Text Value: $TEXT_VALUE" > /tmp/"${{INSTANCE_ID}}"-task_completion.txt
    
    # Copy the input file from S3
    aws s3 cp s3://$FILE_PATH /tmp/
    
    #Copy the script from S3
    aws s3 cp s3://fovus-coding-aws/script/script.py /tmp/
    
    #Execute Script
    cd /tmp
    python script.py 
    FILENAME=$(basename "$FILE_PATH")
    BASENAME=$(basename "$FILE_PATH" .input)
    
    python script.py $FILENAME $ID "$TEXT_VALUE"
    OUTPUT_FILE="${{BASENAME}}.Output"
    OUTPUT_FILE_PATH="fovus-coding-aws/outputs/$OUTPUT_FILE"
    
    
    #Write new output to s3 bucket
    aws s3 cp /tmp/"$OUTPUT_FILE" s3://fovus-coding-aws/outputs/
    
    #Write item to output database
    aws dynamodb put-item \
    --table-name fovusOutputDB \
    --item '{{"id": {{"S": "'"$ID"'"}},"output_file_path": {{"S": "'"$OUTPUT_FILE_PATH"'"}}}}'
    
    aws s3 cp /tmp/"${{INSTANCE_ID}}"-task_completion.txt s3://fovus-coding-aws/logs/${{INSTANCE_ID}}_task_completion.txt
    
    echo "Tasks completed. Terminating instance..."
    
    # Terminate the instance
    aws ec2 terminate-instances --instance-ids $INSTANCE_ID
    """
    try:
        ec2 = boto3.client('ec2')
        instances = ec2.run_instances(
            ImageId="ami-06c68f701d8090592",
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='fovusKeyPair',
            IamInstanceProfile={
                'Name': 'EC2FovusRole'
            },
            UserData=script
        )
        instance_id = instances['Instances'][0]['InstanceId']
        print("New instance creation initiated:", instance_id)
        return {"Message": f"Instance creation initiated. Instance ID: {instance_id}"}
    except Exception as error:
        return {"error": str(error)}