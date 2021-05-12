import boto3
import moto
from main.S3Upload import S3Upload


@moto.mock_s3
def test_s3():
    # create bucket and file in S3
    s3_client = boto3.resource("s3")
    s3_client.create_bucket(Bucket="testsuite_bucket")

    # Uploading zip file for Lambda
    upload_file_instance = S3Upload("trigger_glue.zip", "testsuite_bucket")
    upload_file_instance.upload_script()

    upload_response = s3_client.Object('testsuite_bucket', 'script/trigger_glue.zip').get()[
        'ResponseMetadata']['HTTPStatusCode']
    if upload_response == 200:
        print("trigger_glue.zip file uploaded")

    # Uploading py file for glue
    upload_file_instance = S3Upload("RdsConnection.py", "testsuite_bucket")
    upload_file_instance.upload_script()

    upload_response = s3_client.Object('testsuite_bucket', 'script/RdsConnection.py').get()[
        'ResponseMetadata']['HTTPStatusCode']
    if upload_response == 200:
        print("trigger_glue.py file uploaded")

    # Uploading csv file for lambda trigger
    upload_file_instance = S3Upload("sample_csv.csv", "testsuite_bucket")
    upload_file_instance.upload_csv()

    upload_response = s3_client.Object('testsuite_bucket', 'csv/sample_csv.csv').get()[
        'ResponseMetadata']['HTTPStatusCode']
    if upload_response == 200:
        print("sample_csv.csv file uploaded")


test_s3()
