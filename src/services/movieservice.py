from random import choice

from domain.validators import MovieException
from repository.iterabledatastructure import IterableStructure
from src.domain.movie import Movie


class MovieService:
    def __init__(self, movie_repository, rental_repository):
        """
        Creates a new movie service
        :param movie_repository: The movie repository
        :param rental_repository: The rental repository
        """
        self.__movie_repository = movie_repository
        self.__rental_repository = rental_repository

    @property
    def movie_repository(self):
        return self.__movie_repository

    @property
    def rental_repository(self):
        return self.__rental_repository

    def add(self, movie_id, title, description, genre):
        """
        Adds a new movie to the repository
        :param movie_id: The movie's ID
        :param title: The movie's title
        :param description: The movie's description
        :param genre: The movie's genre
        :return: nothing
        """
        self.movie_repository.add(Movie(movie_id, title, description, genre))

    def add_movie_and_rentals(self, movie_id, title, description, genre, rentals):
        """
        Adds a movie and some of its rentals to the repositories
        :param movie_id: The movie's ID
        :param title: The movie's title
        :param description: The movie's description
        :param genre: The movie's genre
        :param rentals: The movie's rentals
        :return: nothing
        """
        self.add(movie_id, title, description, genre)
        for rental in rentals:
            self.rental_repository.add(rental)

    def get_all_rentals_for_movie(self, movie_id):
        """
        Returns all of the rentals for a given movie
        :param movie_id: The movie's id
        :return: The list of all of the movie's rentals
        """
        return IterableStructure.filter(self.rental_repository.entities, lambda x: x.movie_id == movie_id)

    def remove(self, movie_id):
        """
        Removes a movie from the repository and all it's rentals
        :param movie_id: The ID of the movie to be removed
        :return: A tuple containing the removed movie's attributes and the list of removed rentals
        """
        removed_movie = self.movie_repository.remove(movie_id)
        removed_rentals = self.get_all_rentals_for_movie(movie_id)
        for rental in removed_rentals:
            self.rental_repository.remove(rental.id)
        return removed_movie.id, removed_movie.title, removed_movie.description, removed_movie.genre, removed_rentals

    def update(self, movie_id, new_title, new_description, new_genre):
        """
        Updates a movie from the repository
        :param movie_id: The movie's ID
        :param new_title: The movie's new title
        :param new_description: The movie's new description
        :param new_genre: The movie's new genre
        :return: A tuple containing the old movie's attributes
        """
        old_movie = self.movie_repository.get_entity_at_id(movie_id)
        self.movie_repository.update(Movie(movie_id, new_title, new_description, new_genre))
        return old_movie.id, old_movie.title, old_movie.description, old_movie.genre

    def get_current_list(self):
        """
        Returns the current list of movies
        :return: The current list of movies
        """
        return self.movie_repository.entities

    def search_for_movies_by_everything(self, searching_string):
        """
        Generates the list of movies with attributes containing a given string
        :param searching_string: The given string
        :return: The list of movies with attributes containing a given string
        """
        attribute_list = ["id", "title", "description", "genre"]
        found_movies_list = []
        for attribute in attribute_list:
            movies_with_attribute = self.search_for_movies_by_attribute(searching_string, attribute)
            found_movies_list += IterableStructure.filter(movies_with_attribute,
                                                          lambda x: x not in found_movies_list)
        IterableStructure.sort(found_movies_list, lambda x, y: x.id < y.id)
        return found_movies_list

    def search_for_movies_by_attribute(self, searching_string, attribute):
        """
        Generates the list of movies with a given attribute containing a given string
        :param searching_string: The given string
        :param attribute: The attribute of the client
        :return: The list of movies with the attribute containing the given string
        Raise MovieException if attribute is not id, title, description or genre
        """
        if attribute not in ["id", "title", "description", "genre"]:
            raise MovieException("Invalid attribute!")
        return IterableStructure.filter(self.get_current_list(),
                                        lambda x: searching_string in str(eval("x."+attribute)).lower())

    def generate_starting_movies(self):
        """
        Generates 10 random movies to populate the repository
        :return: nothing
        """
        title_starting_list = ["The Wizard of ", "Lawrence of ", "Sleepless in ", "Gangs of ", "Sweet Home ",
                               "When in ", "Once Upon a Time in ", "What Happens in ", "Midnight in ", "This is "]
        title_ending_list = ["Oz", "Arabia", "Seattle", "New York", "Alabama", "Rome", "Hollywood", "Vegas", "Paris",
                             "England"]
        movie_descriptions = ["The magical adventure of a girl named Dorothy in a strange land",
                              "The story of an English officer who unites different types of people for a common goal",
                              "A man in search of his new love after his wife died",
                              "A story of revenge where a son avenges his father's death",
                              "The story of a woman who must return home in order to divorce her husband",
                              "The story of how magic can lead to love",
                              "Two friends try to achieve fame in 1969",
                              "A man and a woman must live together as a couple in order to not lose a large amount "
                              "of money",
                              "While on a trip with his family, a writer finds himself mysteriously travelling back in "
                              "time",
                              "A young boy becomes part of a gang"]
        movie_genres = ["Adventure", "Biography", "Comedy", "Crime", "Romance", "Drama", "Fantasy", "Sci-Fi",
                        "Thriller", "Horror"]
        for i in range(1, 11):
            self.movie_repository.add(Movie(i, choice(title_starting_list) + choice(title_ending_list),
                                            choice(movie_descriptions), choice(movie_genres)))
