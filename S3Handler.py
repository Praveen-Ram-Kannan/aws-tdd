import os

import boto3

class S3Handler:
    def __init__(self):
        # self.s3_session = boto3.session.Session()
        self.s3_client = boto3.client('s3')
        self.bucket = 'test_bucket'
        self.file = 'test.zip'
        self.file_path = 'C:\\Users\\praveen.ram.kannan\\PycharmProjects\\Django\\test_files'

    def upload_file(self):
        path = os.path.join(self.file_path, self.file)
        self.s3_client.upload_file(path, self.bucket, self.file)