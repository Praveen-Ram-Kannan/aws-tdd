import boto3
import moto


class SnsMoto:

    def __init__(self, message):
        self.message = message

    @moto.mock_sqs
    @moto.mock_sns
    def test_sns_sqs(self):
        sns_client = boto3.client('sns', region_name='us-east-1')
        topic = sns_client.create_topic(Name='awstestsuite-result-sns')
        topic_arn = topic["TopicArn"]

        sqs_client = boto3.resource("sqs", region_name="us-east-1")
        sqs_client.create_queue(QueueName="awstestsuite-result-queue")

        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol="sqs",
            Endpoint="arn:aws:sqs:us-east-1:123456789012:awstestsuite-result-queue",
        )

        # publish message
        sns_client.publish(TopicArn=topic_arn, Message=self.message)

        queue = sqs_client.get_queue_by_name(QueueName="awstestsuite-result-queue")
        messages = queue.receive_messages(MaxNumberOfMessages=1)
        print(messages[0].body)
