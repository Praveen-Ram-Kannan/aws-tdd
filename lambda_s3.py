import os
import boto3
import json


class LambdaHandler:

    def __init__(self):
        self.lambdaClient = boto3.client('lambda')
        self.s3client = self.s3_session.client("s3")
        self.lambdaName = "start_glue_job"
        self.roleName = "arn:aws:iam::672580443112:role/trigger_lambda_glue"
        self.s3_session = boto3.session.Session()
        self.bucket = "test_bucket"
        self.file = "trigger_glue.zip"
        self.file_path = "C:\\Users\\s.b.dhanapalan\\Documents"
        self.principal = "s3.amazonaws.com"
        self.action = "lambda:InvokeFunction"
        self.source_arn = "arn:aws:s3:::sownds3"

    def upload_file(self):
        path = os.path.join(self.file_path, self.file)
        self.s3client.upload_file(path, self.bucket, self.file)

    def create_lambda(self):

        create_lambda_function = self.lambdaClient.create_function(
            FunctionName=self.lambdaName,
            Runtime='python3.8',
            Role=self.roleName,
            Handler='{}.lambda_handler'.format('trigger_glue'),
            Description='trigger a glue job',
            Code={'S3Bucket': 'test_bucket', 'S3Key': 'trigger_glue.zip'}
        )
        return create_lambda_function

    def lambda_add_permission(self):
        response = self.lambdaClient.add_permission(
            FunctionName=self.lambdaName,
            StatementId=1,
            Action=self.action,
            Principal=self.principal,
            SourceArn=self.source_arn
        )
        return response

    def add_trigger(self):
        response = self.s3client.put_bucket_notification_configuration(
            Bucket=self.bucket,
            NotificationConfiguration={'LambdaFunctionConfigurations': [
                {"LambdaFunctionArn": "arn:aws:lambda:us-east-1:672580443112:function:start_glue_job",
                 "Events": ["s3:ObjectCreated:*"]}]}
        )
        return response

    # def invoke_lambda(self):
    #     response = self.lambdaClient.invoke(
    #         FunctionName=self.lambdaName,
    #         InvocationType='RequestResponse',
    #         LogType='Tail',
    #         Payload=json.dumps({'job_name': "lambda_glue_s", 'detail': "lambda to glue trigger"})
    #     )
    #     return response


# lambda_client = boto3.client("lambda")
# lambdaevnt = LambdaHandler()
# lambdaevnt.create_lambda()
# lambdaevnt.invoke_lambda()