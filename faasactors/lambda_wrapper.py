import importlib
import json
import os
import boto3
from faasactors.actor import Actor
from faasactors.utils.config import AWS_REGION

def lambda_wrapper(event, context):

    actor_name = context.function_name
    actor_clazz_name = os.environ['ACTOR_CLASS_NAME']
    actor_module_name = os.environ['ACTOR_MODULE_NAME']
    actor_module = importlib.__import__(actor_module_name)

    clazz = getattr(actor_module, actor_clazz_name)
    a = Actor(actor_name, clazz)
    a.load()

    sqscli = boto3.resource('sqs', region_name=AWS_REGION)
    queue = sqscli.get_queue_by_name(QueueName=actor_name)

    continueReading = True
    while (continueReading):
        list = queue.receive_messages(WaitTimeSeconds=8)
        if len(list) > 0:
            for record in list:
                message = json.loads(record.body)
                assert actor_name == message["TO"]

                method = message["METHOD"]
                args = message["PARAMS"][0]
                kwargs = message["PARAMS"][1]

                a.invoke(method, args, kwargs)
                record.delete()
        else:
            continueReading = False
    print("no more messages")
    a.dump()