"""
CONFIGURATION CONSTANTS
"""

AWS_REGION = 'us-east-1'
# The role needs access to the VPC, Elasticache, lambda, sns, sqs and logs.
AWS_ROLE_ARN = 'arn:aws:iam::786929956471:role/alvaroPickleTest'
VPC_CONFIG = {
    'SubnetIds': [
        'subnet-xxxx',
    ],
    'SecurityGroupIds': [
        'sg-xxxxxx',
    ]
}
# Endpoint for the redis cluster. Elasticache.
REDIS_HOST = 'endpoint.cache.amazonaws.com'
REDIS_PORT = 6379
# An SNS topic for the lambdas to communicate.
TOPIC_ARN = 'arn:aws:sns:region:client:topic'
# SQS queue where to receive the final result.
RESULT_QUEUE = 'queuename'
# Lambda name that does the sort of the map results, and the shuffle to the
# reducers. Create it with the 'new_lambda' function. And the sortnshuffle.py scheme.
SHUFFLER = 'sortnshuffle'
