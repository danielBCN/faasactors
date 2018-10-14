from faasactors.client import spawn
from tests.Ponger import Ponger


class Pinger(object):
    def ping(self):
        ponger = spawn("Ponger", Ponger)
        ponger.pong()