import unittest
from RDS import User


class TestUser(unittest.TestCase):
    def testEqual(self):
        user1 = User("Max Mustermann")
        user2 = User("12345")
        user3 = User("Max Mustermann")

        self.assertNotEqual(user1, user2)
        self.assertEqual(user1, user3)
        self.assertEqual(user3, user1)
        self.assertEqual(user1, user1)
