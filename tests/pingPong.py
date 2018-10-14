from faasactors.client import spawn
from tests.Pinger import Pinger


def main():
    pinger = spawn("Pinger_29", Pinger)
    pinger.ping()


if __name__ == '__main__':
    main()
