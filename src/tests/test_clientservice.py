from datetime import date
from unittest import TestCase

from domain.rental import Rental
from domain.validators import ClientValidator, ClientException, RentalValidator, RentalException
from repository.repo import Repository
from services.clientservice import ClientService


class TestClientService(TestCase):
    def setUp(self):
        self.rental_repo = Repository(RentalValidator, RentalException)
        self.client_service = ClientService(Repository(ClientValidator, ClientException), self.rental_repo)
        self.client_service.add(1, "name")
        self.rental_repo.add(Rental(1, 1, 1, date(2020, 7, 23), date(2020, 8, 23)))

    def test_add(self):
        self.client_service.add(2, "name")
        self.assertEqual(2, len(self.client_service.client_repository.entities))
        self.assertEqual("name", self.client_service.client_repository.entities[1].name)

    def test_add_client_and_rentals(self):
        self.client_service.add_client_and_rentals(2, "name", [Rental(2, 1, 1, date(2020, 8, 24), date(2020, 9, 24))])
        self.assertEqual(2, len(self.client_service.client_repository.entities))
        self.assertEqual(2, len(self.rental_repo.entities))

    def test_get_all_rentals_for_client(self):
        self.assertEqual(1, len(self.client_service.get_all_rentals_for_client(1)))
        self.assertEqual(0, len(self.client_service.get_all_rentals_for_client(0)))

    def test_remove(self):
        self.assertRaises(ClientException, self.client_service.remove, 2)
        self.client_service.remove(1)
        self.assertEqual(0, len(self.client_service.client_repository.entities))
        self.assertEqual(0, len(self.rental_repo.entities))

    def test_update(self):
        self.assertRaises(ClientException, self.client_service.update, 2, "new name")
        self.client_service.update(1, "new name")
        client_position = self.client_service.client_repository.get_current_ids().index(1)
        self.assertEqual("new name", self.client_service.client_repository.entities[client_position].name)

    def test_get_current_list(self):
        self.assertEqual(1, len(self.client_service.get_current_list()))

    def test_generate_starting_clients(self):
        self.client_service.remove(1)
        self.client_service.generate_starting_clients()
        self.assertEqual(10, len(self.client_service.client_repository.entities))

    def test_search_for_clients_by_everything(self):
        self.client_service.add(2, "another name1")
        self.assertEqual(len(self.client_service.search_for_clients_by_everything("1")), 2)
        self.assertEqual(len(self.client_service.search_for_clients_by_everything("name")), 2)
        self.assertEqual(len(self.client_service.search_for_clients_by_everything("ano")), 1)
        self.assertEqual(len(self.client_service.search_for_clients_by_everything("idk")), 0)

    def test_search_for_clients_by_attribute(self):
        self.client_service.add(2, "another name1")
        self.assertEqual(len(self.client_service.search_for_clients_by_attribute("1", "id")), 1)
        self.assertEqual(len(self.client_service.search_for_clients_by_attribute("name", "name")), 2)
        self.assertEqual(len(self.client_service.search_for_clients_by_attribute("ano", "id")), 0)
        self.assertEqual(len(self.client_service.search_for_clients_by_attribute("idk", "id")), 0)
        self.assertRaises(ClientException, self.client_service.search_for_clients_by_attribute, "name", "idk")


