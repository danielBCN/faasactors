import inspect

from .__version__ import __version__
from .actor import Actor, Proxy
from .lambda_wrapper import lambda_wrapper
from .utils.deploy import new_lambda, map_lambda_to_queue, \
    set_lambda_concurrency

actors = {}


def spawn(name, klass, *args, **kwargs):
    actor = Actor(name, klass)
    actor.create(*args, **kwargs)
    actors[name] = actor

    klass_path = inspect.getfile(klass)
    new_lambda(name, lambda_wrapper, actor_path=klass_path)
    set_lambda_concurrency(name, 1)
    map_lambda_to_queue(name, actor._channel.get_queue_arn())

    return Proxy(actor)


def client():
    print("Client OK")
    print(__version__)


if __name__ == '__main__':
    client()
