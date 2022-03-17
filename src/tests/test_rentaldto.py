from unittest import TestCase

from services.rentaldto import MoviesRentedDays, ClientRentedDays, RentalRentedDays


class TestMoviesRentedDays(TestCase):
    def setUp(self):
        self.movie_rented_days = MoviesRentedDays(1, "t", 2)

    def test_movie_id(self):
        self.assertEqual(self.movie_rented_days.movie_id, 1)

    def test_movie_title(self):
        self.assertEqual(self.movie_rented_days.movie_title, "t")

    def test_days(self):
        self.assertEqual(self.movie_rented_days.days, 2)

    def test_str(self):
        self.assertEqual(str(self.movie_rented_days), "Movie ID: 1\nTitle: t\nDays rented: 2\n")


class TestClientRentedDays(TestCase):
    def setUp(self):
        self.client_rented_days = ClientRentedDays(1, "n", 2)

    def test_client_id(self):
        self.assertEqual(self.client_rented_days.client_id, 1)

    def test_client_name(self):
        self.assertEqual(self.client_rented_days.client_name, "n")

    def test_days(self):
        self.assertEqual(self.client_rented_days.days, 2)

    def test_str(self):
        self.assertEqual(str(self.client_rented_days), "Client ID: 1\nName: n\nMovie rental days: 2")


class TestRentalRentedDays(TestCase):
    def setUp(self):
        self.rental_rented_days = RentalRentedDays(1, "t", 2)

    def test_rental_id(self):
        self.assertEqual(self.rental_rented_days.rental_id, 1)

    def test_movie_title(self):
        self.assertEqual(self.rental_rented_days.movie_title, "t")

    def test_days(self):
        self.assertEqual(self.rental_rented_days.days, 2)

    def test_str(self):
        string = "Rental ID: 1\nMovie title: t\nOverdue days: 2"
        self.assertEqual(str(self.rental_rented_days), string)
