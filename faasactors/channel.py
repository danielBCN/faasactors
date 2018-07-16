import boto3

from .utils.config import AWS_REGION

sqscli = boto3.resource('sqs', region_name=AWS_REGION)


class Channel(object):
    def __init__(self, queue_name):
        self.channel_name = queue_name
        # self.queue = sqscli.get_queue_by_name(QueueName=queue_name)
        self.queue = createQueue(queue_name)

    def send(self, msg):
        print("Channel", self.channel_name, "sending ", msg)
        # Create a new message
        # response =
        self.queue.send_message(MessageBody=msg)

    def get_queue_arn(self):
        self.queue.attributes.get('QueueArn')


def createQueue(name):
    """ Create the queue. This returns an SQS.Queue instance. """
    return sqscli.create_queue(
        QueueName=name,
        Attributes={'DelaySeconds': '0'}
    )



