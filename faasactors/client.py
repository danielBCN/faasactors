from .__version__ import __version__
from .actor import Actor, Proxy

actors = {}


def spawn(name, klass, *args, **kwargs):
    actor = Actor(name, klass)
    actor.create(*args, **kwargs)
    actors["name"] = actor

    return Proxy(actor)


def client():
    print("Client OK")
    print(__version__)


if __name__ == '__main__':
    client()
