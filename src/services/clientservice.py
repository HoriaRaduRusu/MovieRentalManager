from random import choice

from domain.validators import ClientException
from repository.iterabledatastructure import IterableStructure
from src.domain.client import Client


class ClientService:
    def __init__(self, client_repository, rental_repository):
        """
        Creates a new client service
        :param client_repository: The client repository
        :param rental_repository: The rental repository
        """
        self.__client_repository = client_repository
        self.__rental_repository = rental_repository

    @property
    def client_repository(self):
        return self.__client_repository

    @property
    def rental_repository(self):
        return self.__rental_repository

    def get_all_rentals_for_client(self, client_id):
        """
        Returns all of the rentals for a given client
        :param client_id: The client's id
        :return: The list of all of the client's rentals
        """
        return IterableStructure.filter(self.rental_repository.entities, lambda x: x.client_id == client_id)

    def add(self, client_id, name):
        """
        Adds a new client to the repository
        :param client_id: The client's ID
        :param name: The client's name
        :return: nothing
        """
        self.client_repository.add(Client(client_id, name))

    def add_client_and_rentals(self, client_id, name, rentals):
        """
        Adds a client and some of his rentals to the repositories
        :param client_id: The client's ID
        :param name: The client's name
        :param rentals: The client's rentals
        :return: nothing
        """
        self.add(client_id, name)
        for rental in rentals:
            self.rental_repository.add(rental)

    def remove(self, client_id):
        """
        Removes a client from the repository and all the client's rentals
        :param client_id: The ID of the client to be removed
        :return: A tuple containing the removed client's attributes and a list of the removed rentals
        """
        removed_client = self.client_repository.remove(client_id)
        removed_rentals = self.get_all_rentals_for_client(client_id)
        for rental in removed_rentals:
            self.rental_repository.remove(rental.id)
        return removed_client.id, removed_client.name, removed_rentals

    def update(self, client_id, new_name):
        """
        Updates a client from the repository
        :param client_id: The ID of the client to be updated
        :param new_name: The client's new name
        :return: A tuple containing the client's old attributes
        """
        old_client = self.client_repository.get_entity_at_id(client_id)
        self.client_repository.update(Client(client_id, new_name))
        return old_client.id, old_client.name

    def get_current_list(self):
        """
        Returns the current list of clients
        :return: The current list of clients
        """
        return self.client_repository.entities

    def search_for_clients_by_everything(self, searching_string):
        """
        Generates the list of clients with attributes contain a given string
        :param searching_string: The given string
        :return: The list of clients with attributes contain the given string
        """
        attribute_list = ["id", "name"]
        found_clients_list = []
        for attribute in attribute_list:
            clients_with_attribute = self.search_for_clients_by_attribute(searching_string, attribute)
            found_clients_list += IterableStructure.filter(clients_with_attribute,
                                                           lambda x: x not in found_clients_list)
        IterableStructure.sort(found_clients_list, lambda x, y: x.id < y.id)
        return found_clients_list

    def search_for_clients_by_attribute(self, searching_string, attribute):
        """
        Generates the list of clients with a given attribute containing a given string
        :param searching_string: The given string
        :param attribute: The attribute of the client
        :return: The list of clients with the attribute containing the given string
        Raise ClientException if attribute is not either id or name
        """
        if attribute not in ["id", "name"]:
            raise ClientException("Invalid attribute!")
        return IterableStructure.filter(self.get_current_list(),
                                        lambda x: searching_string in str(eval("x."+attribute)).lower())

    def generate_starting_clients(self):
        """
        Generates 10 random clients to populate the repository
        :return: nothing
        """
        client_first_names = ["Elijah ", "Axl ", "Ashton ", "Albert ", "Neil ", "Elizabeth ", "Marie ", "Marilyn ",
                              "Greta ", "Jennifer "]
        client_last_names = ["Wood", "Rose", "Kutcher", "Einstein", "Gaiman", "Windsor", "Curie", "Monroe", "Thunberg",
                             "Lopez"]
        for i in range(1, 11):
            self.client_repository.add(Client(i, choice(client_first_names) + choice(client_last_names)))
