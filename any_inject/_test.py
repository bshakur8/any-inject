import unittest

from any_inject import Injector


class A:
    def __init__(self):
        self.x = 5


class InjectorTests(unittest.TestCase):

    def test_sanity(self):
        a = A()
        id1 = hash(a)
        Injector.register_instance("a", a)
        self.assertIn(a, Injector.get_all_instances().values())
        Injector.register_class("best_class", A)
        self.assertIn(A, Injector.get_all_classes().values())
        Atag = Injector.get_class('best_class')
        atag = Atag()
        self.assertEqual(Atag().x, 5)
        self.assertNotEqual(id1, hash(atag))