from datetime import date
from unittest import TestCase

from domain.rental import Rental
from domain.validators import MovieValidator, MovieException, RentalValidator, RentalException
from repository.repo import Repository
from services.movieservice import MovieService


class TestMovieService(TestCase):
    def setUp(self):
        self.rental_repo = Repository(RentalValidator, RentalException)
        self.movie_service = MovieService(Repository(MovieValidator, MovieException), self.rental_repo)
        self.movie_service.add(1, "title", "description", "genre")
        self.rental_repo.add(Rental(1, 1, 1, date(2020, 7, 23), date(2020, 8, 23)))

    def test_add(self):
        self.movie_service.add(2, "title", "description", "genre")
        self.assertEqual(2, len(self.movie_service.movie_repository.entities))
        self.assertEqual("title", self.movie_service.movie_repository.entities[1].title)
        self.assertEqual("description", self.movie_service.movie_repository.entities[1].description)
        self.assertEqual("genre", self.movie_service.movie_repository.entities[1].genre)

    def test_add_movie_and_rentals(self):
        test_rental = Rental(2, 1, 1, date(2020, 8, 24), date(2020, 9, 24))
        self.movie_service.add_movie_and_rentals(2, "title", "description", "genre", [test_rental])
        self.assertEqual(2, len(self.movie_service.movie_repository.entities))
        self.assertEqual(2, len(self.rental_repo.entities))

    def test_get_all_rentals_for_movie(self):
        self.assertEqual(1, len(self.movie_service.get_all_rentals_for_movie(1)))
        self.assertEqual(0, len(self.movie_service.get_all_rentals_for_movie(0)))

    def test_remove(self):
        self.assertRaises(MovieException, self.movie_service.remove, 2)
        self.movie_service.remove(1)
        self.assertEqual(0, len(self.movie_service.movie_repository.entities))
        self.assertEqual(0, len(self.rental_repo.entities))

    def test_update(self):
        self.assertRaises(MovieException, self.movie_service.update, 2, "new title", "new description", "new genre")
        self.movie_service.update(1, "new title", "new description", "new genre")
        movie_position = self.movie_service.movie_repository.get_current_ids().index(1)
        self.assertEqual("new title", self.movie_service.movie_repository.entities[movie_position].title)
        self.assertEqual("new description", self.movie_service.movie_repository.entities[movie_position].description)
        self.assertEqual("new genre", self.movie_service.movie_repository.entities[movie_position].genre)

    def test_get_current_list(self):
        self.assertEqual(1, len(self.movie_service.get_current_list()))

    def test_generate_starting_movies(self):
        self.movie_service.remove(1)
        self.movie_service.generate_starting_movies()
        self.assertEqual(10, len(self.movie_service.movie_repository.entities))

    def test_search_for_movies_by_everything(self):
        self.movie_service.add(2, "another title1", "another description", "another genre")
        self.assertEqual(len(self.movie_service.search_for_movies_by_everything("1")), 2)
        self.assertEqual(len(self.movie_service.search_for_movies_by_everything("title")), 2)
        self.assertEqual(len(self.movie_service.search_for_movies_by_everything("ano")), 1)
        self.assertEqual(len(self.movie_service.search_for_movies_by_everything("idk")), 0)

    def test_search_for_movies_by_attribute(self):
        self.movie_service.add(2, "another title1", "another description", "another genre")
        self.assertEqual(len(self.movie_service.search_for_movies_by_attribute("1", "id")), 1)
        self.assertEqual(len(self.movie_service.search_for_movies_by_attribute("1", "title")), 1)
        self.assertEqual(len(self.movie_service.search_for_movies_by_attribute("title", "title")), 2)
        self.assertEqual(len(self.movie_service.search_for_movies_by_attribute("ano", "id")), 0)
        self.assertEqual(len(self.movie_service.search_for_movies_by_attribute("idk", "title")), 0)
        self.assertRaises(MovieException, self.movie_service.search_for_movies_by_attribute, "title", "idk")
