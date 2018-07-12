from .. import faasactors
from faasactors import actor
import unittest
import inspect


class Dummy(object):

    def method1(self):
        print("m1")

    def method2(self):
        print("m2")


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
