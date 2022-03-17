from unittest import TestCase

from domain.client import Client
from domain.validators import ClientValidator, ClientException
from repository.repo import Repository


class TestRepository(TestCase):
    def setUp(self):
        self.repo = Repository(ClientValidator, ClientException)
        self.test_client = Client(1, "name")
        self.repo.add(self.test_client)

    def test_entities(self):
        self.assertEqual(len(self.repo.entities), 1)

    def test_add(self):
        self.assertEqual(len(self.repo.entities), 1)
        self.assertRaises(ClientException, self.repo.add, Client(1, "name"))
        self.repo.add(Client(2, "another name"))
        self.assertEqual(len(self.repo.entities), 2)

    def test_remove(self):
        self.assertRaises(ClientException, self.repo.remove, 2)
        self.repo.remove(1)
        self.assertEqual(len(self.repo.entities), 0)

    def test_update(self):
        self.assertRaises(ClientException, self.repo.update, Client(2, "name"))
        self.repo.update(Client(1, "another name"))
        current_pos = self.repo.get_current_ids().index(1)
        self.assertEqual(self.repo.entities[current_pos].name, "another name")

    def test_get_current_ids(self):
        self.assertEqual(len(self.repo.get_current_ids()), 1)
        self.repo.add(Client(2, "name"))
        self.assertEqual(self.repo.get_current_ids(), [1, 2])

    def test_get_entity_at_id(self):
        self.assertRaises(ClientException, self.repo.get_entity_at_id, 2)
        self.assertEqual(self.test_client, self.repo.get_entity_at_id(1))
