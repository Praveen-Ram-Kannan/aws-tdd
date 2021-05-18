import boto3
import os
from pathlib import Path


class S3Upload(object):
    def __init__(self, file, bucket):
        self.bucket = bucket
        self.file = file
        self.script_path = os.path.join(Path(__file__).resolve().parents[1], 'main')
        self.csv_path = os.path.join(Path(__file__).resolve().parents[1], 'csv_files')
        self.lambdaName = "Rds_lambda_trigger"
        self.principal = "s3.amazonaws.com"
        self.action = "lambda:InvokeFunction"
        self.source_arn = "arn:aws:s3:::testsuite_bucket"
        self.s3client = boto3.client('s3', region_name='us-east-1')
        self.lambdaClient = boto3.client('lambda')

    def upload_script(self):
        path = os.path.join(self.script_path, self.file)
        key = "script/" + self.file
        self.s3client.upload_file(path, self.bucket, key)

    def upload_csv(self):
        path = os.path.join(self.csv_path, self.file)
        key = "csv/" + self.file
        self.s3client.upload_file(path, self.bucket, key)

    #TODO
    def lambda_add_permission(self):
        self.lambdaClient.add_permission(
            FunctionName=self.lambdaName,
            StatementId=1,
            Action=self.action,
            Principal=self.principal,
            SourceArn=self.source_arn
        )

        self.lambdaClient.get_policy(FunctionName=self.lambdaName)

    def add_trigger(self):
        response = self.s3client.put_bucket_notification_configuration(
            Bucket="testsuite_bucket",
            NotificationConfiguration={'LambdaFunctionConfigurations': [
                {"LambdaFunctionArn": "arn:aws:lambda:us-east-1:672580443112:function:Rds_lambda_trigger",
                 "Events": ["s3:ObjectCreated:*"],
                 'Filter': {
                     'Key': {
                         'FilterRules': [
                             {
                                 'Name': 'csv/' | '.csv',
                             }
                         ]
                     }
                 }
                 }]}

        )
        return response
