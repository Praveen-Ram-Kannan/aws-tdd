# aws-tdd
Dependent packages
1. moto
2. boto3

Windows Docker - https://docs.docker.com/docker-for-windows/install/
Linux Kernel - https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package

# TestCase Covered

S3
    
    Testcase 1 : validate table creation
    Testcase 2 : validate file upload
    Testcase 3 : validate file content


Lambda

    Testcase 1 : validate Lambda Function creation
    Testcase 2 : validate lambda Invocation


RDS

    Testcase 1 : validate DB instance creation
    Testcase 2 : Validate Start and Stop Function

SNS

    Testcase 1 : validate SNS Topic Creation
    Testcase 2 : validate Topic Supscription

SQS

    Testcase 1 : validate Queue Creation
    Testcase 2 : validate Message Received from SNS  