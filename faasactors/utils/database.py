import inspect
import json

import boto3

from .config import AWS_REGION, ACTOR_TABLE_NAME

dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
dynamodb_resource = boto3.resource('dynamodb', region_name=AWS_REGION)
table = None


def create_actor_table():
    try:
        # response = \
        dynamodb.create_table(
            TableName=ACTOR_TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'actorID',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'actorID',
                    'AttributeType': 'S'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except dynamodb.exceptions.ResourceInUseException:
        print("Table already exists.")
    global table
    table = dynamodb_resource.Table(ACTOR_TABLE_NAME)


def create_actor_entry(actor_name, actor_instance):
    attrs = get_instance_attributes(actor_instance)
    table.put_item(
        Item={
            'actorID': actor_name,
            'attributes': json.dumps(attrs),
        }
    )


def load_actor(actor_name, actor_instance):
    response = table.get_item(
        Key={'actorID': actor_name}
    )
    attrs = json.loads(response['Item']['attributes'])
    for att, val in attrs.items():
        setattr(actor_instance, att, val)
    return actor_instance


def dump_actor(actor_name, actor_instance):
    attrs = get_instance_attributes(actor_instance)
    table.update_item(
        Key={'actorID': actor_name},
        AttributeUpdates={
            'attributes': {'Value': json.dumps(attrs)},
        }
    )


def get_instance_attributes(instance):
    return dict([(n, a) for n, a in
                 inspect.getmembers(instance, lambda x: not inspect.ismethod(x))
                 if '__' not in n])
