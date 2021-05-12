import os
import boto3
import json


class LambdaHandler:

    def __init__(self):
        self.lambdaclient = boto3.client('lambda', region_name='us-east-1')
        self.lambdaname = "start_glue_job"

    def create_lambda(self):
        create_lambda_function = self.lambdaclient.create_function(
            FunctionName=self.lambdaname,
            Runtime='python3.8',
            Role='arn:aws:iam::123456789012:role/my-path/test_role',
            Handler='{}.lambda_handler'.format('trigger_glue'),
            Description='trigger a glue job',
            Code={'S3Bucket': 'test_bucket', 'S3Key': 'trigger_glue.zip'})

    def invoke_lambda(self):
        response = self.lambdaclient.invoke(
            FunctionName=self.lambdaname,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps({'job_name': "lambda_glue_s", 'detail': "lambda to glue trigger"})
        )
        return response
