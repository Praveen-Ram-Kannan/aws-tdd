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
        self.lambdaClient = boto3.client('lambda', region_name='us-east-1')

    def upload_script(self):
        path = os.path.join(self.script_path, self.file)
        key = "script/" + self.file
        self.s3client.upload_file(path, self.bucket, key)

    def upload_obj(self):
        path = os.path.join(self.csv_path, self.file)
        key = "file/" + self.file
        csv_response = self.s3client.put_object(Body="test_obj", Bucket=self.bucket, Key=key)

        return csv_response
