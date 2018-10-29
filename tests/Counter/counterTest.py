from faasactors.client import spawn
from tests.Counter.Counter import Counter


def main():
    actor = spawn("Counter", Counter)
    actor.increment()
    if __name__ == '__main__':
        main()