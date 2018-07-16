from faasactors.client import spawn
from tests.ActorX import ActorX


def main():
    actor = spawn("myActor", ActorX)

    actor.say_hello()


if __name__ == '__main__':
    main()
