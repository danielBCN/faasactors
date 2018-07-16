"""
Utils to create lambda functions.
"""
import uuid
import boto3

from .packaging import package_with_dependencies
from .config import AWS_ROLE_ARN, AWS_REGION, LAMBDA_UPDATE

lambdacli = boto3.client('lambda', region_name=AWS_REGION)


def uuid_str():
    """ Generate an unique id."""
    return str(uuid.uuid4())


def new_lambda(name, handler, actor_path):
    """
    Packages all files that the function *handler* depends on into a zip.
    Creates a new lambda with name *name* on AWS using that zip.
    This one does not have VPC config. So it has acces to extern services
    such as SNS and SQS. (But can't connect directly to Redis)
    """
    # zip function-module and dependencies
    zipfile, lamhand = package_with_dependencies(handler,
                                                 extra_modules=[actor_path])

    # create the new lambda by uploading the zip.
    try:
        response = lambdacli.create_function(
            FunctionName=name,
            Runtime='python3.6',
            Role=AWS_ROLE_ARN,
            Handler=lamhand,
            Code={'ZipFile': zipfile.getvalue()},
            Publish=True,
            Description='Lambda with cloud object.',
            Timeout=29,
            MemorySize=128
            # VpcConfig=VPC_CONFIG,
            # DeadLetterConfig={
            #     'TargetArn': 'string'
            # },
            #  Environment={
            #    'Variables': {  # FIXME: Variables should be requested. Timeout too.
            #        'ACTOR_CLASS_NAME': Actor
            #    }
            #  }
            # KMSKeyArn='string',
            # TracingConfig={
            #     'Mode': 'Active'|'PassThrough'
            # },
            # Tags={
            #     'string': 'string'
            # }
        )
        # print(response)
        print(f"New lambda {name} created successfully.")
    except lambdacli.exceptions.ResourceConflictException:
        print("Lambda already exists...")
        if LAMBDA_UPDATE:
            print("Updating Lambda...")
            delete_lambda(name)
            new_lambda(name, handler, actor_path)
        else:
            print("*NO* Lambda update. Proceeding...")


def delete_lambda(name):
    """ Deletes a lambda function from AWS with name *name*."""
    response = lambdacli.delete_function(FunctionName=name)
    # print(response)
    print(f"Lambda {name} deleted successfully.")


def set_lambda_concurrency(name, concurrency_value):
    """ Sets the maximum amount of concurrent executions to a lambda
     function with name *name*."""
    response = lambdacli.put_function_concurrency(
        FunctionName=name,
        ReservedConcurrentExecutions=concurrency_value
    )
    # print(response)
    print(f"Lambda {name} concurrency limit set"
          f" to {concurrency_value} successfully.")


def map_lambda_to_queue(lambda_name, queue_arn):
    try:
        lambdacli.create_event_source_mapping(
            EventSourceArn=queue_arn,
            FunctionName=lambda_name,
        )
    except lambdacli.exceptions.ResourceConflictException:
        print("Trigger mapping already exists. Skipping...")
