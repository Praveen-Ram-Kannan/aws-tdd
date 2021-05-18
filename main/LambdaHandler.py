import boto3
import json


class LambdaHandler:

    def __init__(self):
        self.lambda_client = boto3.client('lambda', region_name='us-east-1')
        self.lambda_name = "Rds_lambda_trigger"

    def create_lambda(self):
        self.lambda_client.create_function(
            FunctionName=self.lambda_name,
            Runtime='python3.8',
            Role='arn:aws:iam::123456789012:role/my-path/test_role',
            Handler='{}.test_create_database'.format('RdsConnection'),
            Description='create Rds instance',
            Code={'S3Bucket': 'testsuite_bucket', 'S3Key': 'script/Rds_lambda_trigger.zip'})

    def invoke_lambda(self):
        response = self.lambda_client.invoke(
            FunctionName=self.lambda_name,
            InvocationType='Event',
            LogType='Tail',
        )
        return response
