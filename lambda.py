from LambdaHandler import LambdaHandler
from S3Handler import S3Handler
import moto
import boto3
import docker


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
def test_mocklambda():
    test_iamrole()
    # create bucket and file in S3
    s3_client = boto3.client("s3")
    s3_client.create_bucket(Bucket="test_bucket")
    s3evnt = S3Handler()
    s3evnt.upload_file()

    # create lambda
    lambda_client = boto3.client("lambda", region_name='us-east-1')
    lambdaevnt = LambdaHandler()
    lambdaevnt.create_lambda()
    response = lambdaevnt.invoke_lambda()
    response1 = lambda_client.list_functions()



test_mocklambda()
