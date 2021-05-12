import boto3
import os
from pathlib import Path


class S3Upload(object):
    def __init__(self, file, bucket):
        self.bucket = bucket
        self.file = file
        self.script_path = os.path.join(Path(__file__).resolve().parents[1], 'main')
        self.csv_path = os.path.join(Path(__file__).resolve().parents[1], 'csv_files')

    def upload_script(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        path = os.path.join(self.script_path, self.file)
        key = "script/" + self.file
        s3.upload_file(path, self.bucket, key)

    def upload_csv(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        path = os.path.join(self.csv_path, self.file)
        key = "csv/" + self.file
        s3.upload_file(path, self.bucket, key)

    # def add_trigger(self):
    #     response = self.s3client.put_bucket_notification_configuration(
    #         Bucket=self.bucket,
    #         NotificationConfiguration={'LambdaFunctionConfigurations': [
    #             {"LambdaFunctionArn": "arn:aws:lambda:us-east-1:672580443112:function:start_glue_job",
    #              "Events": ["s3:ObjectCreated:*"],
    #              'Filter': {
    #                  'Key': {
    #                      'FilterRules': [
    #                          {
    #                              'Name': 'csv',
    #                          }
    #                      ]
    #                  }
    #              }
    #              }]}
    #
    #     )
    #     return response