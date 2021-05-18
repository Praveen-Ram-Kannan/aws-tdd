import boto3
import moto
import json
from SnsMoto import SnsMoto


@moto.mock_rds2
def test_create_database(event, context):
    conn = boto3.client("rds", region_name="us-east-1")
    database = conn.create_db_instance(
        DBInstanceIdentifier="postgres-cluster",
        AllocatedStorage=10,
        Engine="postgres",
        DBName="testsuite",
        DBInstanceClass="db.t2.micro",
        MasterUsername="AwsTestSuite",
        MasterUserPassword="testsuite",
        Port=5432,
        DBSecurityGroups=["my_sg"],
        VpcSecurityGroupIds=["sg-123456"],
    )

    instances = conn.describe_db_instances(
        DBInstanceIdentifier=database["DBInstance"]["DBInstanceIdentifier"]
    )["DBInstances"][0]

    if instances["DBInstanceStatus"]:
        print("RDS test case 1 : Instance is  created & available")

    response = conn.stop_db_instance(
        DBInstanceIdentifier=instances["DBInstanceIdentifier"],
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200 and \
            response["DBInstance"]["DBInstanceStatus"] == 'stopped':
        print("RDS test case 2 : Instance is stopped")

    response = conn.start_db_instance(DBInstanceIdentifier=instances["DBInstanceIdentifier"])
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200 and \
            response["DBInstance"]["DBInstanceStatus"] == 'available':
        print("RDS test case 3 : Instance is available")

    # Publish message to SNS
    message = json.dumps({
        "HTTPStatusCode": response["ResponseMetadata"]["HTTPStatusCode"],
        "instances_availability": response["DBInstance"]["DBInstanceStatus"]

    })

    SnsMoto_obj = SnsMoto(message)
    SnsMoto_obj.test_sns_sqs()

    return message
