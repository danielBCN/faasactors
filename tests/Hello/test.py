from faasactors.client import spawn
from tests.Hello.ActorX import ActorX


def main():
    actor = spawn("myActor1", ActorX)

    actor.say_hello()


if __name__ == '__main__':
    main()
