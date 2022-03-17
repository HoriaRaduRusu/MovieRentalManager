from datetime import date
from unittest import TestCase

from domain.client import Client
from domain.movie import Movie
from domain.rental import Rental
from domain.validators import MovieValidator, ClientValidator, ClientException, MovieException, RentalException, \
    RentalValidator
from repository.repo import Repository
from services.clientservice import ClientService
from services.handlers import Handlers
from services.movieservice import MovieService
from services.rentalservice import RentalService


class TestHandlers(TestCase):
    def setUp(self):
        self.client_repo = Repository(ClientValidator, ClientException)
        self.movie_repo = Repository(MovieValidator, MovieException)
        self.rental_repo = Repository(RentalValidator, RentalException)
        self.client_service = ClientService(self.client_repo, self.rental_repo)
        self.movie_service = MovieService(self.movie_repo, self.rental_repo)
        self.rental_service = RentalService(self.client_repo, self.movie_repo, self.rental_repo)
        self.client_repo.add(Client(1, "n1"))
        self.client_repo.add(Client(2, "n2"))
        self.client_repo.add(Client(3, "n3"))
        self.movie_repo.add(Movie(1, "t1", "d1", "g1"))
        self.movie_repo.add(Movie(2, "t2", "d2", "g2"))
        self.movie_repo.add(Movie(3, "t3", "d3", "g3"))
        self.movie_repo.add(Movie(4, "t4", "d4", "g4"))
        self.test_rental1 = Rental(1, 1, 1, date(2020, 5, 23), date(2020, 7, 23))
        self.rental_repo.add(self.test_rental1)
        self.test_rental2 = Rental(2, 2, 2, date(2020, 5, 23), date(2020, 7, 23), date(2020, 8, 23))
        self.rental_repo.add(self.test_rental2)
        self.test_rental3 = Rental(3, 1, 2, date(2020, 4, 23), date(2020, 5, 22), date(2020, 4, 27))
        self.rental_repo.add(self.test_rental3)

    def test_remove_client_handler(self):
        Handlers.remove_client_handler(self.client_service, 1)
        self.assertEqual(2, len(self.client_repo.entities))

    def test_add_client_handler(self):
        Handlers.add_client_handler(self.client_service, 4, "n4")
        self.assertEqual(4, len(self.client_repo.entities))

    def test_add_client_and_rentals_handler(self):
        test_rental4 = Rental(4, 1, 4, date(2020, 7, 23), date(2020, 8, 23))
        Handlers.add_client_and_rentals_handler(self.client_service, 4, "n4", [test_rental4])
        self.assertEqual(4, len(self.client_repo.entities))
        self.assertEqual(4, len(self.rental_repo.entities))

    def test_update_client_handler(self):
        Handlers.update_client_handler(self.client_service, 1, "new_name")
        self.assertEqual("new_name", self.client_repo.get_entity_at_id(1).name)

    def test_remove_movie_handler(self):
        Handlers.remove_movie_handler(self.movie_service, 1)
        self.assertEqual(3, len(self.movie_repo.entities))

    def test_add_movie_handler(self):
        Handlers.add_movie_handler(self.movie_service, 5, "t5", "d5", "g5")
        self.assertEqual(5, len(self.movie_repo.entities))

    def test_add_movie_and_rentals_handler(self):
        test_rental4 = Rental(4, 5, 1, date(2020, 7, 23), date(2020, 8, 23))
        Handlers.add_movie_and_rentals_handler(self.movie_service, 5, "t5", "d5", "g5", [test_rental4])
        self.assertEqual(5, len(self.movie_repo.entities))
        self.assertEqual(4, len(self.rental_repo.entities))

    def test_update_movie_handler(self):
        Handlers.update_movie_handler(self.movie_service, 1, "new_title", "new_desc", "new_genre")
        self.assertEqual("new_title", self.movie_repo.get_entity_at_id(1).title)
        self.assertEqual("new_desc", self.movie_repo.get_entity_at_id(1).description)
        self.assertEqual("new_genre", self.movie_repo.get_entity_at_id(1).genre)

    def test_delete_rental_handler(self):
        Handlers.delete_rental_handler(self.rental_service, 1)
        self.assertEqual(2, len(self.rental_repo.entities))

    def test_cancel_return_handler(self):
        Handlers.cancel_return_handler(self.rental_service, 2)
        self.assertIsNone(self.rental_repo.get_entity_at_id(2).returned_date)

    def test_add_rental_handler(self):
        Handlers.add_rental_handler(self.rental_service, 4, 1, 1, date(2020, 3, 24), date(2020, 4, 20))
        self.assertEqual(4, len(self.rental_repo.entities))

    def test_return_movie_handler(self):
        Handlers.return_movie_handler(self.rental_service, 1, date(2020, 11, 30))
        self.assertEqual(date(2020, 11, 30), self.rental_repo.get_entity_at_id(1).returned_date)
