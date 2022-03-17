from unittest import TestCase

from domain.movie import Movie


class TestMovie(TestCase):
    def setUp(self):
        self.movie = Movie(1, "title", "description", "genre")

    def test_id(self):
        self.assertEqual(self.movie.id, 1)

    def test_title(self):
        self.assertEqual(self.movie.title, "title")

    def test_description(self):
        self.assertEqual(self.movie.description, "description")

    def test_genre(self):
        self.assertEqual(self.movie.genre, "genre")

    def test_str(self):
        string = "---------- ID: 1 ----------\nTitle: title\nDescription: description\nGenre: genre"
        self.assertEqual(str(self.movie), string)
