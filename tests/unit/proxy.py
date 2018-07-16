from .. import faasactors
from faasactors import actor
import unittest
import inspect

from .dummy import Dummy


class TestBasic(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_proxy_methods(self):
        a = actor.Actor("actor", Dummy)
        a.create()
        p = actor.Proxy(a)
        print(p.__dict__)
        p.method1()

        methods = inspect.getmembers(p, lambda x: isinstance(x, actor.TellWrapper))
        print(methods)

