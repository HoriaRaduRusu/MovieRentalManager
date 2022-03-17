import abc
from datetime import datetime

from domain.client import Client
from domain.movie import Movie
from domain.rental import Rental


class JSONDataAccess(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def deserializer(self, dictionary):
        pass

    @abc.abstractmethod
    def serializer(self, entity):
        pass


class ClientJSONDataAccess(JSONDataAccess):
    def deserializer(self, dictionary):
        """
        Transforms a dictionary into a Client object
        :param dictionary: The dictionary containing the attributes of the Client object
        :return: The corresponding Client object
        """
        return Client(*dictionary.values())

    def serializer(self, entity):
        """
        Transforms a Client object into a dictionary
        :param entity: The Client object that will be converted to a dictionary
        :return: The corresponding dictionary
        """
        return {"id": entity.id, "name": entity.name}


class MovieJSONDataAccess(JSONDataAccess):

    def deserializer(self, dictionary):
        """
        Transforms a dictionary into a Movie object
        :param dictionary: The dictionary containing the attributes of the Movie object
        :return: The corresponding Movie object
        """
        return Movie(*dictionary.values())

    def serializer(self, entity):
        """
        Transforms a Movie object into a dictionary
        :param entity: The Movie object that will be converted to a dictionary
        :return: The corresponding dictionary
        """
        return {"id": entity.id, "title": entity.title, "description": entity.description, "genre": entity.genre}


class RentalJSONDataAccess(JSONDataAccess):

    def deserializer(self, dictionary):
        """
        Transforms a dictionary into a Rental object
        :param dictionary: The dictionary containing the attributes of the Rental object
        :return: The corresponding Rental object
        """
        rented_date = datetime.strptime(dictionary["rented_date"], "%Y-%m-%d").date()
        due_date = datetime.strptime(dictionary["due_date"], "%Y-%m-%d").date()
        if dictionary["returned_date"] != "None":
            returned_date = datetime.strptime(dictionary["returned_date"], "%Y-%m-%d").date()
        else:
            returned_date = None
        return Rental(dictionary["id"], dictionary["movie_id"], dictionary["client_id"], rented_date, due_date,
                      returned_date)

    def serializer(self, entity):
        """
        Transforms a Rental object into a dictionary
        :param entity: The Rental object that will be converted to a dictionary
        :return: The corresponding dictionary
        """
        rented_date = str(entity.rented_date)
        due_date = str(entity.due_date)
        returned_date = str(entity.returned_date)
        return {"id": entity.id, "movie_id": entity.movie_id, "client_id": entity.client_id, "rented_date": rented_date,
                "due_date": due_date, "returned_date": returned_date}
