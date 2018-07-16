from .. import faasactors
import unittest
import inspect

from .dummy import Dummy
from faasactors.utils import database


class TestBasic(unittest.TestCase):
    def setUpClass(cls):
        database.create_actor_table()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_attributes(self):
        members = inspect.getmembers(Dummy(), lambda x: not inspect.ismethod(x))
        attrs = [(n, f) for n, f in members if '__' not in n]
        self.assertTrue(attrs == [('attr', 0), ('attrK', 0)])
        print(str(dict(attrs)))

    def test_create_actor_item(self):
        dummy = Dummy()
        dummy.attrK = 123
        database.create_actor_entry("DummyActor", dummy)

    def test_update_actor_item(self):
        dummy = Dummy()
        dummy.attrK = 321
        database.dump_actor("DummyActor", dummy)

    def test_get_actor_item(self):
        dummy = Dummy()
        database.load_actor("DummyActor", dummy)
        print(dummy.attrK)
