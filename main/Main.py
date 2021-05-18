import boto3
import moto
from main.S3Upload import S3Upload
from main.LambdaHandler import LambdaHandler


@moto.mock_iam
def test_iamrole():
    # create IAM role
    iam_client = boto3.client('iam')
    iam_client.create_role(
        Path='/my-path/',
        RoleName='test_role',
        AssumeRolePolicyDocument='some policy',
        Description='string',
    )


@moto.mock_lambda
@moto.mock_s3
def test_main():
    # Create iam Role
    test_iamrole()

    # create bucket and file in S3
    s3_client = boto3.resource("s3")
    s3_client.create_bucket(Bucket="testsuite_bucket")

    # Uploading zip file for Lambda
    upload_file_instance = S3Upload("Rds_lambda_trigger.zip", "testsuite_bucket")
    upload_file_instance.upload_script()

    upload_response = s3_client.Object('testsuite_bucket', 'script/Rds_lambda_trigger.zip').get()[
        'ResponseMetadata']['HTTPStatusCode']
    if upload_response == 200:
        print("Rds_lambda_trigger.zip file uploaded")

    # Uploading py file for glue
    # upload_file_instance = S3Upload("RdsConnection.py", "testsuite_bucket")
    # upload_file_instance.upload_script()
    #
    # upload_response = s3_client.Object('testsuite_bucket', 'script/RdsConnection.py').get()[
    #     'ResponseMetadata']['HTTPStatusCode']
    # if upload_response == 200:
    #     print("trigger_glue.py file uploaded")

    # Create Lambda Function
    lambda_client = boto3.client("lambda", region_name='us-east-1')
    lambda_event = LambdaHandler()
    lambda_event.create_lambda()
    function_nm = lambda_client.list_functions()

    if function_nm["Functions"][0]["FunctionName"] == "Rds_lambda_trigger":
        print("lambda function " + str(function_nm["Functions"][0]["FunctionName"]) + " created")
    lambda_response = lambda_event.invoke_lambda()
    print(lambda_response)
    if "FunctionError" in lambda_response:
        print(lambda_response["Payload"].read().decode("utf-8"))

    # Uploading csv file for lambda trigger
    upload_file_instance = S3Upload("sample_csv.csv", "testsuite_bucket")
    upload_file_instance.upload_csv()

    upload_response = s3_client.Object('testsuite_bucket', 'csv/sample_csv.csv').get()[
        'ResponseMetadata']['HTTPStatusCode']
    if upload_response == 200:
        print("sample_csv.csv file uploaded")


if __name__ == "__main__":
    # Main Function
    test_main()
