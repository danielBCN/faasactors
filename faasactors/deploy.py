"""
Utils to create lambda functions.
"""
import uuid
import boto3


from faasactors.utils.packaging import package_with_dependencies
from faasactors.config import (AWS_ROLE_ARN, VPC_CONFIG, REDIS_HOST, REDIS_PORT, TOPIC_ARN,
                    AWS_REGION, RESULT_QUEUE, SHUFFLER)


lambdacli = boto3.client('lambda', region_name=AWS_REGION)
sqscli = boto3.resource('sqs', region_name=AWS_REGION)


def uuid_str():
    """ Generate an uninque id."""
    return str(uuid.uuid4())


def get_lambda_client():
    """ Just returns a boto3 lambda client connection."""
    return lambdacli


def new_lambda(name, handler):
    """
    Packages all files that the function *handler* depends on into a zip.
    Creates a new lambda with name *name* on AWS using that zip.
    This one does not have VPC config. So it has acces to extern services
    such as SNS and SQS. (But can't connect directly to Redis)
    """
    # zip function-module and dependencies
    zipfile, lamhand = package_with_dependencies(handler)

    # create the new lambda by uploading the zip.
    response = lambdacli.create_function(
        FunctionName=name,
        Runtime='python3.6',
        Role=AWS_ROLE_ARN,
        Handler=lamhand,
        Code={'ZipFile': zipfile.getvalue()},
        Publish=True,
        Description='Lambda with cloud object.',
        Timeout=60,
        MemorySize=128
        # VpcConfig=VPC_CONFIG,
        # DeadLetterConfig={
        #     'TargetArn': 'string'
        # },
        #  Environment={
        #    'Variables': {  # FIXME: Variables should be requested. Timeout too.
        #        'RESULT_QUEUE': RESULT_QUEUE
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
    print(response)
    print("New lambda {} created successfully.".format(name))


def delete_lambda(name):
    """ Deletes a lambda function from AWS with name *name*."""
    response = lambdacli.delete_function(FunctionName=name)
    print(response)
    print("Lambda {} deleted successfully.".format(name))


def set_lambda_concurrency(name, concurrency_value):
    """ Sets the maximum amount of concurrent executions to a lambda function with name *name*."""
    response = lambdacli.put_function_concurrency(FunctionName=name, ReservedConcurrentExecutions=concurrency_value)
    print(response)
    print("Lambda {} concurrency limit set to {} successfully.".format(name, concurrency_value))
