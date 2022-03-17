import abc
import sqlite3
from datetime import datetime

from domain.client import Client
from domain.movie import Movie
from domain.rental import Rental


class SQLDataAccess(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read_from_line(self, attribute_tuple):
        pass

    @abc.abstractmethod
    def add(self, entity, file):
        pass

    @abc.abstractmethod
    def remove(self, entity_id, file):
        pass

    @abc.abstractmethod
    def update(self, entity, file):
        pass


class ClientSQLDataAccess(SQLDataAccess):

    def read_from_line(self, attribute_tuple):
        return Client(*attribute_tuple)

    def add(self, entity, file):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO clients VALUES(?, ?)",
                       (entity.id, entity.name))
        connection.commit()
        connection.close()

    def remove(self, entity_id, file):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM clients "
                       "WHERE ID=?",
                       (entity_id, ))
        connection.commit()
        connection.close()

    def update(self, entity, file):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("UPDATE clients "
                       "SET Name = ? "
                       "WHERE ID = ? ",
                       (entity.name, entity.id))
        connection.commit()
        connection.close()


class MovieSQLDataAccess(SQLDataAccess):

    def read_from_line(self, attribute_tuple):
        return Movie(*attribute_tuple)

    def add(self, entity, file):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO movies "
                       "VALUES(?, ?, ?, ?)",
                       (entity.id, entity.title, entity.description, entity.genre))
        connection.commit()
        connection.close()

    def remove(self, entity_id, file):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM movies "
                       "WHERE ID=?",
                       (entity_id, ))
        connection.commit()
        connection.close()

    def update(self, entity, file):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("UPDATE movies "
                       "SET Title = ?, Description = ?, Genre = ?"
                       "WHERE ID = ?",
                       (entity.title, entity.description, entity.genre, entity.id))
        connection.commit()
        connection.close()


class RentalSQLDataAccess(SQLDataAccess):

    def read_from_line(self, attribute_tuple):
        rented_date = datetime.strptime(attribute_tuple[3], "%Y-%m-%d").date()
        due_date = datetime.strptime(attribute_tuple[4], "%Y-%m-%d").date()
        if attribute_tuple[5] != "None":
            returned_date = datetime.strptime(attribute_tuple[5], "%Y-%m-%d").date()
        else:
            returned_date = None
        return Rental(attribute_tuple[0], attribute_tuple[1], attribute_tuple[2], rented_date, due_date, returned_date)

    def add(self, entity, file):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO rentals "
                       "VALUES(?, ?, ?, ?, ?, ?)",
                       (entity.id, entity.movie_id, entity.client_id, str(entity.rented_date),
                        str(entity.due_date), str(entity.returned_date)))
        connection.commit()
        connection.close()

    def remove(self, entity_id, file):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM rentals "
                       "WHERE ID=?",
                       (entity_id, ))
        connection.commit()
        connection.close()

    def update(self, entity, file):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("UPDATE rentals "
                       "SET MovieID = ?, ClientID = ?, RentedDate = ?, DueDate = ?, ReturnedDate = ?"
                       "WHERE ID = ?",
                       (entity.movie_id, entity.client_id, str(entity.rented_date), str(entity.due_date),
                        str(entity.returned_date), entity.id))
        connection.commit()
        connection.close()
