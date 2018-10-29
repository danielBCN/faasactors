from faasactors.client import lookup, spawn

class Pinger(object):
    def ping(self, self_name, target_name, counter):
        if counter > 0:
            ponger = lookup(target_name, Ponger)
            ponger.pong(target_name, self_name, counter - 1)
            print("counter: ", counter)
        else:
            print("counter reached 0")


class Ponger(object):
    def pong(self, self_name, target_name, counter):
        pinger = lookup(target_name, Pinger)
        pinger.ping(target_name, self_name, counter)
        print("ponger says pong")


def main():
    pinger = spawn("Pinger", Pinger)
    ponger = spawn("Ponger", Ponger)
    pinger.ping(pinger.actor_name,ponger.actor_name, 3)


if __name__ == '__main__':
    main()