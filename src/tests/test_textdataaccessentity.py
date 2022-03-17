from datetime import date
from unittest import TestCase

from domain.client import Client
from domain.movie import Movie
from domain.rental import Rental
from repository.textdataaccessentity import ClientTextDataAccess, MovieTextDataAccess, RentalTextDataAccess


class TestClientTextDataAccess(TestCase):
    def setUp(self):
        self.text_file = "../../TestFiles/test_clients_data_access.txt"
        self.client_data_access = ClientTextDataAccess()

    def test_read_from(self):
        with open(self.text_file, "wt") as f:
            f.write("1;Marie Wood")
        with open(self.text_file, "rt") as f:
            readline = f.readline()
        read_client = self.client_data_access.read_from(readline)
        self.assertEqual(read_client.id, 1)
        self.assertEqual(read_client.name, "Marie Wood")

    def test_write_to(self):
        with open(self.text_file, "wt") as f:
            self.client_data_access.write_to(f, Client(2, "Carie Wood"))

        with open(self.text_file, "rt") as f:
            readline = f.readline()
        read_client = self.client_data_access.read_from(readline)
        self.assertEqual(read_client.id, 2)
        self.assertEqual(read_client.name, "Carie Wood")


class TestMovieTextDataAccess(TestCase):
    def setUp(self):
        self.text_file = "../../TestFiles/test_movie_data_access.txt"
        self.movie_data_access = MovieTextDataAccess()

    def test_read_from(self):
        with open(self.text_file, "wt") as f:
            f.write("1;title;description;genre")
        with open(self.text_file, "rt") as f:
            readline = f.readline()
        read_movie = self.movie_data_access.read_from(readline)
        self.assertEqual(read_movie.id, 1)
        self.assertEqual(read_movie.title, "title")
        self.assertEqual(read_movie.description, "description")
        self.assertEqual(read_movie.genre, "genre")

    def test_write_to(self):
        with open(self.text_file, "wt") as f:
            self.movie_data_access.write_to(f, Movie(2, "title2", "description2", "genre2"))

        with open(self.text_file, "rt") as f:
            readline = f.readline()
        read_movie = self.movie_data_access.read_from(readline)
        self.assertEqual(read_movie.id, 2)
        self.assertEqual(read_movie.title, "title2")
        self.assertEqual(read_movie.description, "description2")
        self.assertEqual(read_movie.genre, "genre2")


class TestRentalTextDataAccess(TestCase):
    def setUp(self):
        self.text_file = "../../TestFiles/test_rental_data_access.txt"
        self.rental_data_access = RentalTextDataAccess()

    def test_read_from(self):
        with open(self.text_file, "wt") as f:
            f.write("1;1;6;2019-09-24;2019-10-18;2019-10-05")
        with open(self.text_file, "rt") as f:
            readline = f.readline()
        read_rental = self.rental_data_access.read_from(readline)
        self.assertEqual(read_rental.id, 1)
        self.assertEqual(read_rental.movie_id, 1)
        self.assertEqual(read_rental.client_id, 6)
        self.assertEqual(read_rental.rented_date, date(2019, 9, 24))
        self.assertEqual(read_rental.due_date, date(2019, 10, 18))
        self.assertEqual(read_rental.returned_date, date(2019, 10, 5))

    def test_write_to(self):
        rented_date = date(2019, 9, 25)
        due_date = date(2019, 10, 19)
        returned_date = date(2019, 10, 6)
        with open(self.text_file, "wt") as f:
            self.rental_data_access.write_to(f, Rental(2, 2, 7, rented_date, due_date, returned_date))

        with open(self.text_file, "rt") as f:
            readline = f.readline()
        read_rental = self.rental_data_access.read_from(readline)
        self.assertEqual(read_rental.id, 2)
        self.assertEqual(read_rental.movie_id, 2)
        self.assertEqual(read_rental.client_id, 7)
        self.assertEqual(read_rental.rented_date, rented_date)
        self.assertEqual(read_rental.due_date, due_date)
        self.assertEqual(read_rental.returned_date, returned_date)

