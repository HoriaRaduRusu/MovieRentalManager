from unittest import TestCase

from domain.client import Client


class TestClient(TestCase):
    def setUp(self):
        self.client = Client(1, "name")

    def test_name(self):
        self.assertEqual(self.client.name, "name")

    def test_id(self):
        self.assertEqual(self.client.id, 1)

    def test_str(self):
        string = "---------- ID: 1 ----------\nName: name"
        self.assertEqual(str(self.client), string)
