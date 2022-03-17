from datetime import date
from unittest import TestCase

from domain.client import Client
from domain.movie import Movie
from domain.rental import Rental
from domain.validators import ClientValidator, ClientException, MovieValidator, MovieException, RentalException, \
    RentalValidator, InvalidDateException, InvalidOptionException, LateClientException, RentedMovieException, \
    UndoRedoException


class TestClientValidator(TestCase):
    def setUp(self):
        self.client1 = Client("a", "name")
        self.client2 = Client(-1, "name")
        self.client3 = Client(1, 1)
        self.client4 = Client(1, "name")

    def test_validate(self):
        self.assertRaises(ClientException, ClientValidator.validate, self.client1)
        self.assertRaises(ClientException, ClientValidator.validate, self.client2)
        self.assertRaises(ClientException, ClientValidator.validate, self.client3)
        self.assertIsNone(ClientValidator.validate(self.client4))


class TestMovieValidator(TestCase):
    def setUp(self):
        self.movie1 = Movie("a", "title", "description", "genre")
        self.movie2 = Movie(-1, "title", "description", "genre")
        self.movie3 = Movie(1, 1, "description", "genre")
        self.movie4 = Movie(1, "title", 1, "genre")
        self.movie5 = Movie(1, "title", "description", 1)
        self.movie6 = Movie(1, "title", "description", "genre")

    def test_validate(self):
        self.assertRaises(MovieException, MovieValidator.validate, self.movie1)
        self.assertRaises(MovieException, MovieValidator.validate, self.movie2)
        self.assertRaises(MovieException, MovieValidator.validate, self.movie3)
        self.assertRaises(MovieException, MovieValidator.validate, self.movie4)
        self.assertRaises(MovieException, MovieValidator.validate, self.movie5)
        self.assertIsNone(MovieValidator.validate(self.movie6))


class TestRentalValidator(TestCase):
    def setUp(self):
        self.rental1 = Rental("a", 1, 1, date(2020, 5, 12), date(2020, 6, 12), date(2020, 5, 28))
        self.rental2 = Rental(-1, 1, 1, date(2020, 5, 12), date(2020, 6, 12), date(2020, 5, 28))
        self.rental3 = Rental(1, "a", 1, date(2020, 5, 12), date(2020, 6, 12), date(2020, 5, 28))
        self.rental4 = Rental(1, -1, 1, date(2020, 5, 12), date(2020, 6, 12), date(2020, 5, 28))
        self.rental5 = Rental(1, 1, "a", date(2020, 5, 12), date(2020, 6, 12), date(2020, 5, 28))
        self.rental6 = Rental(1, 1, -1, date(2020, 5, 12), date(2020, 6, 12), date(2020, 5, 28))
        self.rental7 = Rental(1, 1, 1, 1, date(2020, 6, 12), date(2020, 5, 28))
        self.rental8 = Rental(1, 1, 1, date(2020, 5, 12), 1, date(2020, 5, 28))
        self.rental9 = Rental(1, 1, 1, date(2020, 5, 12), date(2020, 6, 12), 1)
        self.rental10 = Rental(1, 1, 1, date(2020, 5, 12), date(2020, 4, 12), date(2020, 5, 28))
        self.rental11 = Rental(1, 1, 1, date(2020, 5, 12), date(2020, 6, 12), date(2020, 4, 28))
        self.rental12 = Rental(1, 1, 1, date(2020, 5, 12), date(2020, 6, 12))

    def test_validate(self):
        self.assertRaises(RentalException, RentalValidator.validate, self.rental1)
        self.assertRaises(RentalException, RentalValidator.validate, self.rental2)
        self.assertRaises(RentalException, RentalValidator.validate, self.rental3)
        self.assertRaises(RentalException, RentalValidator.validate, self.rental4)
        self.assertRaises(RentalException, RentalValidator.validate, self.rental5)
        self.assertRaises(RentalException, RentalValidator.validate, self.rental6)
        self.assertRaises(RentalException, RentalValidator.validate, self.rental7)
        self.assertRaises(RentalException, RentalValidator.validate, self.rental8)
        self.assertRaises(RentalException, RentalValidator.validate, self.rental9)
        self.assertRaises(RentalException, RentalValidator.validate, self.rental10)
        self.assertRaises(RentalException, RentalValidator.validate, self.rental11)
        self.assertIsNone(RentalValidator.validate(self.rental12))


class TestExceptions(TestCase):
    def setUp(self):
        self.exc1 = InvalidDateException("message1")
        self.exc2 = InvalidOptionException("message2")
        self.exc3 = ClientException("message3")
        self.exc4 = MovieException("message4")
        self.exc5 = RentalException("message5")
        self.exc6 = LateClientException("message6")
        self.exc7 = RentedMovieException("message7")
        self.exc8 = UndoRedoException("message8")

    def test_str(self):
        self.assertEqual(str(self.exc1), "message1")
        self.assertEqual(str(self.exc2), "message2")
        self.assertEqual(str(self.exc3), "message3")
        self.assertEqual(str(self.exc4), "message4")
        self.assertEqual(str(self.exc5), "message5")
        self.assertEqual(str(self.exc6), "message6")
        self.assertEqual(str(self.exc7), "message7")
        self.assertEqual(str(self.exc8), "message8")