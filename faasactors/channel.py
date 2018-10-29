import json
import subprocess
import sys

import boto3

from faasactors.utils.config import AWS_REGION

sqscli = boto3.resource('sqs', region_name=AWS_REGION)


class Channel(object):
    def __init__(self, queue_name):
        self.channel_name = queue_name
        self.queue = create_queue(queue_name)
        self.url = boto3.client("sqs").list_queues( QueueNamePrefix=self.channel_name).get('QueueUrls')[0]

    def send(self, msg):
        # Create a new message
        self.queue.send_message(MessageBody=json.dumps(msg))

    def sendRepeated(self, msg, times_repeated):
        # Invokes go program to repeat message efficiently
        subprocess.run(["pwd"])

        subprocess.run(["go", "run",
                        "sqsSender.go",
                        json.dumps(msg),
                        self.url,
                        str(times_repeated)]
                       )

    def get_queue_arn(self):
        return self.queue.attributes.get('QueueArn')


def create_queue(name):
    """ Create the queue. This returns an SQS.Queue instance. """
    return sqscli.create_queue(
        QueueName=name,
        Attributes={'DelaySeconds': '0'}
    )



