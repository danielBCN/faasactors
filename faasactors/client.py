import inspect

import boto3
from faasactors.utils.config import AWS_REGION
from faasactors.__version__ import __version__
from faasactors.actor import Actor, Proxy, ProxyRef
from faasactors.lambda_wrapper import lambda_wrapper
from faasactors.utils.deploy import new_lambda

actors = {}


def spawn(name, klass, times_repeated=0 ,*args, **kwargs):
    actor = Actor(name, klass)
    actor.create(*args, **kwargs)
    actors[name] = actor

    # TEMPORARY (TESTING)
    klass_path = inspect.getfile(klass)
    module = inspect.getmodulename(klass_path)
    new_lambda(name, lambda_wrapper, klass_path, klass.__name__, module)

    # Not used in hybrid solution
    # map_lambda_to_queue(name, actor._channel.get_queue_arn())

    # invoke
    client = boto3.client('lambda', region_name=AWS_REGION)

    client.invoke(FunctionName=name, InvocationType='Event')

    return Proxy(actor, times_repeated)

def lookup(actor_name, klass):

    return ProxyRef(actor_name, klass)

def client():
    print("Client OK")
    print(__version__)

#
# if __name__ == '__main__':
#     client()
