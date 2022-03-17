from datetime import date
from unittest import TestCase

from domain.rental import Rental


class TestRental(TestCase):
    def setUp(self) -> None:
        self.rental = Rental(1, 1, 1, date(2000, 12, 20), date(2000, 12, 25))

    def test_id(self):
        self.assertEqual(self.rental.id, 1)

    def test_movie_id(self):
        self.assertEqual(self.rental.movie_id, 1)

    def test_client_id(self):
        self.assertEqual(self.rental.client_id, 1)

    def test_rented_date(self):
        self.assertEqual(self.rental.rented_date, date(2000, 12, 20))

    def test_due_date(self):
        self.assertEqual(self.rental.due_date, date(2000, 12, 25))

    def test_returned_date(self):
        self.assertIsNone(self.rental.returned_date)
        self.rental.returned_date = date(2000, 12, 21)
        self.assertEqual(self.rental.returned_date, date(2000, 12, 21))

    def test_str(self):
        string = "---------- ID: 1 ----------\nMovie ID: 1\nClient ID: 1\n"
        string += "Rented Date: " + str(date(2000, 12, 20)) + "\nDue Date: " + str(date(2000, 12, 25))
        string += "\nReturned Date: Not Returned"
        self.assertEqual(str(self.rental), string)
