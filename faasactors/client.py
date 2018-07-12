from .__version__ import __version__
from .actor import Actor, Proxy

def client():
    print("Client OK")
    print(__version__)


actors = {}


def spawn(name, klass, *args, **kwargs):
    actor = Actor(name, klass)
    actor.create(*args, **kwargs)
    actors["name"] = actor

    return Proxy(actor)


if __name__ == '__main__':
    client()
