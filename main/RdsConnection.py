import boto3
import moto


@moto.mock_rds2
def test_create_database():
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

    print("Instance created")

    instances = conn.describe_db_instances(
        DBInstanceIdentifier=database["DBInstance"]["DBInstanceIdentifier"]
    )["DBInstances"][0]

    if instances["DBInstanceStatus"]:
        print("Instance is available")

    response = conn.stop_db_instance(
        DBInstanceIdentifier=instances["DBInstanceIdentifier"],
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print("Instance started")
    if response["DBInstance"]["DBInstanceStatus"] == 'stopped':
        print("Instance is stopped")

    response = conn.start_db_instance(DBInstanceIdentifier=instances["DBInstanceIdentifier"])
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print("Instance started")
    if response["DBInstance"]["DBInstanceStatus"] == 'available':
        print("Instance is available")


test_create_database()
