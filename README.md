
# Fovus Coding Challenge Submission

## Basic Requirements Checklist

- [x] Use AWS CDK to manage all AWS infrastructure
- [x] Use AWS SDK JavaScript V3 for Lambda
- [x] Do not put any AWS access key / credentials anwwhere in code
    - All interaction with lambda functions is done through API Gateway
- [x] No SSH and no hard-coded parameters
- [x] Your parameter/variable names, file names, and folder names are reader-friendly and professional
- [x] Your file in s3 is not public
- [x] Do not use any AWS amplify frontend or backend resources
- [x] Follow the AWS best practices
- [x] After saving the inputs and S3 path in DynamoDB filetable, your system will create a new VM based on the event (not a pre-provisioned VM) and trigger the script to run automatically with error handling (no sleep)
- [x] Professional code and reader-friendly README file

## FIle Structure
Javascript backend functions (that interact with API gateway and lambda functions) are in aws-react-app/src/api

Lambda functions that are triggered via DynamoDB stream and API Gateway are in backend folder

React APP Frontend is in aws-react-app/src/App.js and aws-react-app/src/App.css


## Extra Features

React app displays live contents of the database. Input vs Output database can be toggled, as well as refreshed.

## Deployment

1. Clone into repository
2. cd into aws-react-app
3. npm install
4. npm start

A test input file is available in the backend folder

## DEMO
https://youtu.be/oJlGFd0PHoQ

## Resources
https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-dynamo-db.html

https://aws.plainenglish.io/create-ec2-instances-with-lambda-a0a885e2b295

https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html

https://medium.com/@brianhulela/upload-files-to-aws-s3-bucket-from-react-using-pre-signed-urls-543cca728ab8

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.Lambda.html

https://react.dev/













   
