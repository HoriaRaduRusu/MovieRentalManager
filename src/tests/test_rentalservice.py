from datetime import date
from unittest import TestCase

from domain.client import Client
from domain.movie import Movie
from domain.rental import Rental
from domain.validators import ClientValidator, ClientException, MovieValidator, MovieException, RentalValidator, \
    RentalException, LateClientException, RentedMovieException
from repository.repo import Repository
from services.rentalservice import RentalService


class TestRentalService(TestCase):
    def setUp(self):
        self.client_repo = Repository(ClientValidator, ClientException)
        self.movie_repo = Repository(MovieValidator, MovieException)
        self.rental_repo = Repository(RentalValidator, RentalException)
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

    def test_client_repo(self):
        self.assertEqual(self.rental_service.client_repo, self.client_repo)

    def test_movie_repo(self):
        self.assertEqual(self.rental_service.movie_repo, self.movie_repo)

    def test_rental_repo(self):
        self.assertEqual(self.rental_service.rental_repo, self.rental_repo)

    def test_get_current_list(self):
        self.assertEqual(len(self.rental_service.get_current_list()), 3)
        self.assertIn(self.test_rental1, self.rental_service.get_current_list())

    def test_get_client_name(self):
        self.assertEqual(self.rental_service.get_client_name(1), "n1")
        self.assertRaises(ClientException, self.rental_service.get_client_name, 0)
        self.assertRaises(ClientException, self.rental_service.get_client_name, "a")

    def test_get_rentals_from_client(self):
        self.assertRaises(ClientException, self.rental_service.get_rentals_from_client, 0)
        self.assertEqual(1, len(self.rental_service.get_rentals_from_client(1)))
        self.assertEqual(self.test_rental1, self.rental_service.get_rentals_from_client(1)[0])
        self.assertEqual(2, len(self.rental_service.get_rentals_from_client(2)))
        self.assertEqual(0, len(self.rental_service.get_rentals_from_client(3)))

    def test_check_if_client_has_late_returns_at_date(self):
        self.assertTrue(self.rental_service.check_if_client_has_late_returns_at_date(1, date(2020, 11, 24)))
        self.assertTrue(self.rental_service.check_if_client_has_late_returns_at_date(2, date(2020, 11, 24)))
        self.assertFalse(self.rental_service.check_if_client_has_late_returns_at_date(1, date(2020, 6, 23)))
        self.assertFalse(self.rental_service.check_if_client_has_late_returns_at_date(3, date(2020, 11, 24)))
        self.assertFalse(self.rental_service.check_if_client_has_late_returns_at_date(2, date(2020, 6, 24)))

    def test_get_movie_title(self):
        self.assertEqual(self.rental_service.get_movie_title(1), "t1")
        self.assertRaises(MovieException, self.rental_service.get_movie_title, "a")
        self.assertRaises(MovieException, self.rental_service.get_movie_title, 0)

    def test_get_movie_title_from_rental_with_id(self):
        self.assertEqual(self.rental_service.get_movie_title_from_rental_with_id(1), "t1")
        self.assertRaises(RentalException, self.rental_service.get_movie_title_from_rental_with_id, 0)
        self.assertRaises(RentalException, self.rental_service.get_movie_title_from_rental_with_id, "a")

    def test_get_rentals_for_movie(self):
        self.assertRaises(MovieException, self.rental_service.get_rentals_for_movie, 0)
        self.assertEqual(len(self.rental_service.get_rentals_for_movie(1)), 2)
        self.assertEqual(self.test_rental1, self.rental_service.get_rentals_for_movie(1)[0])
        self.assertEqual(0, len(self.rental_service.get_rentals_for_movie(3)))

    def test_check_if_movie_is_available_between_dates(self):
        date1 = date(2020, 8, 24)
        date2 = date(2020, 8, 23)
        date3 = date(2020, 7, 23)
        self.assertFalse(self.rental_service.check_if_movie_is_available_between_dates(1, date2, date1))
        self.assertFalse(self.rental_service.check_if_movie_is_available_between_dates(2, date3, date1))
        self.assertTrue(self.rental_service.check_if_movie_is_available_between_dates(3, date3, date2))

    def test_add_rental(self):
        self.assertRaises(LateClientException, self.rental_service.add_rental,
                          4, 2, 1, date(2020, 8, 23), date(2020, 9, 23))
        self.assertRaises(RentedMovieException, self.rental_service.add_rental,
                          4, 1, 3, date(2020, 8, 23), date(2020, 9, 23))
        self.rental_service.add_rental(4, 3, 3, date(2020, 4, 23), date(2020, 5, 23))
        self.assertEqual(len(self.rental_service.get_current_list()), 4)

    def test_delete_rental(self):
        self.rental_service.delete_rental(1)
        self.assertEqual(2, len(self.rental_repo.entities))
        self.assertRaises(RentalException, self.rental_service.get_movie_title_from_rental_with_id, 1)

    def test_return_movie(self):
        self.assertRaises(RentalException, self.rental_service.return_movie, 4, date(2020, 5, 7))
        self.assertRaises(RentalException, self.rental_service.return_movie, 2, date(2020, 5, 12))
        self.rental_service.return_movie(1, date(2020, 8, 23))
        self.assertEqual(self.rental_repo.get_entity_at_id(1).returned_date, date(2020, 8, 23))

    def test_cancel_return(self):
        self.assertRaises(RentalException, self.rental_service.cancel_return, 4)
        self.assertRaises(RentalException, self.rental_service.cancel_return, 1)
        self.rental_service.cancel_return(2)
        self.assertIsNone(self.rental_repo.get_entity_at_id(2).returned_date)

    def test_generate_random_date(self):
        self.assertRaises(ValueError, self.rental_service.generate_random_date, date(2020, 7, 7), date(2020, 5, 7))
        random_date = self.rental_service.generate_random_date(date(2020, 5, 7), date(2020, 7, 7))
        self.assertGreaterEqual(random_date, date(2020, 5, 7))
        self.assertGreaterEqual(date(2020, 7, 7), random_date)

    def test_generate_starting_rentals(self):
        self.rental_repo.remove(1)
        self.rental_repo.remove(2)
        self.rental_repo.remove(3)
        self.rental_service.generate_starting_rentals()
        self.assertEqual(len(self.rental_service.get_current_list()), 10)

    def test_generate_most_rented_movies(self):
        most_rented_movies = self.rental_service.generate_most_rented_movies()
        self.assertEqual(len(most_rented_movies), 2)
        self.assertEqual(most_rented_movies[0].movie_title, "t1")
        self.assertEqual(most_rented_movies[1].movie_title, "t2")
        self.assertEqual(most_rented_movies[1].days, 92)

    def test_generate_most_active_clients(self):
        most_active_clients = self.rental_service.generate_most_active_clients()
        self.assertEqual(len(most_active_clients), 2)
        self.assertEqual(most_active_clients[0].client_name, "n1")
        self.assertEqual(most_active_clients[1].client_name, "n2")
        self.assertEqual(most_active_clients[1].days, 96)

    def test_generate_late_rentals(self):
        late_rentals = self.rental_service.generate_late_rentals()
        self.assertEqual(len(late_rentals), 1)
        self.assertEqual(late_rentals[0].movie_title, "t1")
