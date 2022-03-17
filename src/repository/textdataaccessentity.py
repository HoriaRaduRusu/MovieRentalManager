import abc
from datetime import date

from domain.client import Client
from domain.movie import Movie
from domain.rental import Rental


class TextDataAccessEntity(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read_from(self, line):
        pass

    @abc.abstractmethod
    def write_to(self, file, entity):
        pass


class ClientTextDataAccess(TextDataAccessEntity):
    def read_from(self, line):
        """
        Reads a string containing an encoded Client entity and creates that entity
        :param line: The string containing the encoded Client
        :return: The corresponding Client entity
        """
        client_id, name = line.strip("\n").split(";")
        return Client(int(client_id), name)

    def write_to(self, file, entity):
        """
        Writes the encoded form of a Client entity to a file
        :param file: The File object in which the Client will be written, open for writing
        :param entity: The Client that will be written to the file
        :return: nothing
        """
        file.write(str(entity.id) + ";" + entity.name + "\n")


class MovieTextDataAccess(TextDataAccessEntity):
    def read_from(self, line):
        """
        Reads a string containing an encoded Movie entity and creates that entity
        :param line: The string containing the encoded Movie
        :return: The corresponding Movie entity
        """
        movie_id, title, description, genre = line.strip("\n").split(";")
        return Movie(int(movie_id), title, description, genre)

    def write_to(self, file, entity):
        """
        Writes the encoded form of a Movie entity to a file
        :param file: The File object in which the Movie will be written, open for writing
        :param entity: The Movie that will be written to the file
        :return: nothing
        """
        file.write(str(entity.id) + ";" + entity.title + ";" + entity.description + ";" + entity.genre + "\n")


class RentalTextDataAccess(TextDataAccessEntity):
    def read_from(self, line):
        """
        Reads a string containing an encoded Rental entity and creates that entity
        :param line: The string containing the encoded Rental
        :return: The corresponding Rental entity
        """
        rental_id, movie_id, client_id, rented_date, due_date, returned_date = line.split(";")
        rented_date = rented_date.strip("\n").split("-")
        rented_date = date(*[int(number) for number in rented_date])
        due_date = due_date.split("-")
        due_date = date(*[int(number) for number in due_date])
        if returned_date == "None":
            returned_date = None
        else:
            returned_date = returned_date.split("-")
            returned_date = date(*[int(number) for number in returned_date])
        return Rental(int(rental_id), int(movie_id), int(client_id), rented_date, due_date, returned_date)

    def write_to(self, file, entity):
        """
        Writes the encoded form of a Rental entity to a file
        :param file: The File object in which the Rental will be written, open for writing
        :param entity: The Rental that will be written to the file
        :return: nothing
        """
        file.write(str(entity.id) + ";" + str(entity.movie_id) + ";" + str(entity.client_id) + ";")
        file.write(str(entity.rented_date) + ";" + str(entity.due_date) + ";" + str(entity.returned_date) + "\n")
