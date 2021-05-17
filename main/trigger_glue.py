import boto3
import moto


@moto.mock_glue
def test_create_glue():
    client = boto3.client('glue', region_name="us-east-1")
    client.create_job(
        Name='trigger_rds_instance',
        Role='arn:aws:iam::123456789012:role/my-path/test_role',
        Command={
            'ScriptLocation': 's3://testsuite_bucket/script/RdsConnection.py',
            'PythonVersion': '3'
        }
    )


test_create_glue()
