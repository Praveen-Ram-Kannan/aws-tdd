import boto3
import moto


@moto.mock_glue
def test_create_glue():
    client = boto3.client('glue', region_name="us-east-1")
    client.create_job(
        Name='trigger_rds_instance',
        Command={
            'ScriptLocation': 'string',
            'PythonVersion': '3'
        },
    )
