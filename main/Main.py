import boto3
import moto
from main.S3Upload import S3Upload
from main.LambdaHandler import LambdaHandler
from main.SnsMoto import SnsMoto


@moto.mock_iam
def test_iam_role():
    # create IAM role
    iam_client = boto3.client('iam', region_name='us-east-1')
    iam_client.create_role(
        Path='/my-path/',
        RoleName='test_role',
        AssumeRolePolicyDocument='some policy',
        Description='string',
    )


@moto.mock_lambda
@moto.mock_s3
@moto.mock_sns
@moto.mock_sqs
def test_main():
    # Create iam Role
    test_iam_role()

    # create bucket and file in S3
    s3_client = boto3.resource("s3", region_name='us-east-1')
    s3_response = s3_client.create_bucket(Bucket="testsuite_bucket")
    print("S3 Test Case 1 : ", s3_response)

    # Uploading zip file for Lambda
    upload_file_instance = S3Upload("Rds_lambda_trigger.zip", "testsuite_bucket")
    upload_file_instance.upload_script()

    upload_response = s3_client.Object('testsuite_bucket', 'script/Rds_lambda_trigger.zip').get()[
        'ResponseMetadata']['HTTPStatusCode']
    if upload_response == 200:
        print("S3 Test Case 2 : Rds_lambda_trigger.zip file uploaded")

    # Uploading csv file for data validation
    expected_result = "test_obj"
    upload_file_instance = S3Upload("sample_file.txt", "testsuite_bucket")
    upload_file_instance.upload_obj()
    actual_result = s3_client.Object("testsuite_bucket", "file/sample_file.txt").get()["Body"].read().decode()

    if expected_result == actual_result:
        print("S3 Test Case 3 : File Content Matches ")

    # Create Lambda Function
    lambda_client = boto3.client("lambda", region_name='us-east-1')
    lambda_event = LambdaHandler()
    lambda_event.create_lambda()
    function_nm = lambda_client.list_functions()

    if function_nm["Functions"][0]["FunctionName"] == "Rds_lambda_trigger":
        print("Lambda Test Case 1 : " + str(function_nm["Functions"][0]["FunctionName"]) + " created")

    lambda_response = lambda_event.invoke_lambda()
    print("Lambda Test Case 2 HTTPStatusCode : ", lambda_response["ResponseMetadata"]["HTTPStatusCode"])

    if "FunctionError" in lambda_response:
        print("Lambda triggered But Error occurred when executing the method ",
              lambda_response["Payload"]._raw_stream.read().decode("utf-8"))
    else:
        print("Lambda triggered with response : ",
              lambda_response["Payload"]._raw_stream.read().decode("utf-8"))


if __name__ == "__main__":
    # Main Function
    test_main()
