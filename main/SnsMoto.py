import boto3


class SnsMoto:

    def __init__(self):
        self.sns_client = boto3.client('sns', region_name='us-east-1')
        self.sqs_client = boto3.resource("sqs", region_name="us-east-1")

    def create_sns_sqs(self, message):
        topic = self.sns_client.create_topic(Name='awstestsuite-result-sns')
        topic_arn = topic["TopicArn"]
        sns_1 = "SNS Test Case 1 : Topic created '" + topic_arn + "'"

        queue = self.sqs_client.create_queue(QueueName="awstestsuite-result-queue")
        sqs_1 = "SQS Test Case 1 : Queue Url '" + str(queue) + "'"

        subscribe_response = self.sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol="sqs",
            Endpoint="arn:aws:sqs:us-east-1:123456789012:awstestsuite-result-queue",
        )

        sns_2 = "SNS Test Case 2 : SubscriptionArn : '" + str(subscribe_response["SubscriptionArn"]) + \
                "'HTTPStatusCode : " + str(subscribe_response["ResponseMetadata"]["HTTPStatusCode"])

        # publish message
        self.sns_client.publish(TopicArn=topic_arn,
                                Message=message)

        queue = self.sqs_client.get_queue_by_name(QueueName="awstestsuite-result-queue")
        sqs_message = queue.receive_messages(MaxNumberOfMessages=1)
        sqs_2 = "SQS Test case 2 Final message :" + str(sqs_message[0].body)

        return sns_1, sns_2, sqs_1, sqs_2
