from datetime import date, timedelta
from random import choice, randint

from domain.rental import Rental
from domain.validators import LateClientException, RentedMovieException, ClientException, MovieException, \
    RentalException
from repository.iterabledatastructure import IterableStructure
from services.rentaldto import MoviesRentedDays, ClientRentedDays, RentalRentedDays


class RentalService:
    def __init__(self, client_repo, movie_repo, rental_repo):
        """
        Generates a new rental service
        :param client_repo: The client repository
        :param movie_repo: The movie repository
        :param rental_repo: The rental repository
        """
        self.__client_repo = client_repo
        self.__movie_repo = movie_repo
        self.__rental_repo = rental_repo

    @property
    def client_repo(self):
        return self.__client_repo

    @property
    def movie_repo(self):
        return self.__movie_repo

    @property
    def rental_repo(self):
        return self.__rental_repo

    def get_current_list(self):
        """
        Returns the current list of rentals
        :return: The list of current rentals
        """
        return self.rental_repo.entities

    def get_client_name(self, client_id):
        """
        Gets the name of a client with a given ID
        :param client_id: The ID of the client
        :return: The client's name
        """
        return self.client_repo.get_entity_at_id(client_id).name

    def get_rentals_from_client(self, client_id):
        """
        Generates a list of all of a client's rentals
        :param client_id: The client's ID
        :return: A list of the given client's rentals
        Raise ClientException if the client does not exist
        """
        if client_id not in self.client_repo.get_current_ids():
            raise ClientException("The client does not exist!")
        return IterableStructure.filter(self.rental_repo.entities, lambda x: x.client_id == client_id)

    def check_if_client_has_late_returns_at_date(self, client_id, rental_date):
        """
        Checks if a client has any late returns that stops him from renting new movies at a given date
        :param client_id: The client's ID
        :param rental_date: The date of the rental
        :return: True if the client has late returns, otherwise False
        """
        rentals_from_client = self.get_rentals_from_client(client_id)
        for rental in rentals_from_client:
            if rental.returned_date is not None:
                if rental.due_date < rental.returned_date and rental.due_date < rental_date:
                    return True
            elif rental.due_date < rental_date:
                return True
        return False

    def get_movie_title(self, movie_id):
        """
        Gets the title of a movie with a given ID
        :param movie_id: The ID of the movie
        :return: The movie's title
        """
        return self.movie_repo.get_entity_at_id(movie_id).title

    def get_movie_title_from_rental_with_id(self, rental_id):
        """
        Gets the movie title from a given rental ID
        :param rental_id: The ID of the rental
        :return: The title of the movie rented in the given rental
        """
        return self.get_movie_title(self.rental_repo.get_entity_at_id(rental_id).movie_id)

    def get_rentals_for_movie(self, movie_id):
        """
        Generates a list of all of the rentals for a given movie
        :param movie_id: The movie's ID
        :return: A list of the rentals for the movie with the given ID
        Raise MovieException if the movie does not exist
        """
        if movie_id not in self.movie_repo.get_current_ids():
            raise MovieException("The movie does not exist!")
        return IterableStructure.filter(self.rental_repo.entities, lambda x: x.movie_id == movie_id)

    def check_if_movie_is_available_between_dates(self, movie_id, rental_date, due_date):
        """
        Checks if a movie is available at every date in a given interval of time
        :param movie_id: The movie's ID
        :param rental_date: The date of the rental
        :param due_date: The due date of the rental
        :return: False if the movie is not available, otherwise True
        """
        rentals_for_movie = self.get_rentals_for_movie(movie_id)
        for rental in rentals_for_movie:
            if rental.returned_date is None:
                if rental.rented_date < rental_date:
                    return False
            elif rental.returned_date > rental_date and rental.rented_date < due_date:
                return False
        return True

    def add_rental(self, rental_id, movie_id, client_id, rented_date, due_date):
        """
        Adds a new rental to the repository
        :param rental_id: The rental's ID
        :param movie_id: The movie's ID
        :param client_id: The client's ID
        :param rented_date: The rental's date
        :param due_date: The rental's due date
        :return: nothing
        Raise LateClientException if the given client has late returns and cannot rent new movies
        Raise RentedMovieException if the given movie is not available
        """
        if self.check_if_client_has_late_returns_at_date(client_id, rented_date):
            raise LateClientException("The client cannot rent any movies, since they returned one late!")
        if not self.check_if_movie_is_available_between_dates(movie_id, rented_date, due_date):
            raise RentedMovieException("The movie is not available!")
        self.rental_repo.add(Rental(rental_id, movie_id, client_id, rented_date, due_date))

    def delete_rental(self, rental_id):
        """
        Deletes a rental from the repository
        :param rental_id: The ID of the rental to be deleted
        :return: nothing
        """
        self.rental_repo.remove(rental_id)

    def return_movie(self, rental_id, return_date):
        """
        Returns a rental
        :param rental_id: The rental's ID
        :param return_date: The date of the return
        :return: nothing
        Raise RentalException if the given rental does not exist or if it has already been returned
        """
        if rental_id not in self.rental_repo.get_current_ids():
            raise RentalException("The rental does not exist!")
        old_rental = self.rental_repo.get_entity_at_id(rental_id)
        if old_rental.returned_date is not None:
            raise RentalException("The rental has already been returned!")
        updated_rental = Rental(rental_id, old_rental.movie_id, old_rental.client_id, old_rental.rented_date,
                                old_rental.due_date, return_date)
        self.rental_repo.update(updated_rental)

    def cancel_return(self, rental_id):
        """
        Cancels a rental's return by setting its return date to None
        :param rental_id: The ID of the rental whose return will be canceled
        :return: nothing
        Raise RentalException if the given rental does not exist or if it has not been returned already
        """
        if rental_id not in self.rental_repo.get_current_ids():
            raise RentalException("The rental does not exist!")
        old_rental = self.rental_repo.get_entity_at_id(rental_id)
        if old_rental.returned_date is None:
            raise RentalException("The rental hasn't been returned!")
        old_rental = self.rental_repo.get_entity_at_id(rental_id)
        updated_rental = Rental(rental_id, old_rental.movie_id, old_rental.client_id, old_rental.rented_date,
                                old_rental.due_date, None)
        self.rental_repo.update(updated_rental)

    @staticmethod
    def generate_random_date(start, end):
        """
        Generates a random date between two given dates
        :param start: The starting date of the interval
        :param end: The ending date of the interval
        :return: A random date between the two
        Raise ValueError if the starting date is bigger than the ending date
        """
        if start > end:
            raise ValueError("The starting date cannot be bigger than the ending date!")
        return start + timedelta(days=randint(0, (end - start).days))

    def generate_starting_rentals(self):
        """
        Generates 10 random rentals to populate the repository
        :return: nothing
        """
        client_ids = list(self.client_repo.get_current_ids())
        movie_ids = list(self.movie_repo.get_current_ids())
        for i in range(1, 11):
            client = choice(client_ids)
            starting_date = self.generate_random_date(date(2018, 1, 1), date.today())
            due_date = starting_date + timedelta(days=randint(1, 60))
            while self.check_if_client_has_late_returns_at_date(client, starting_date):
                client = choice(client_ids)
            movie = choice(movie_ids)
            while not self.check_if_movie_is_available_between_dates(movie, starting_date, due_date):
                movie = choice(movie_ids)
            if due_date < date.today():
                returned_date = self.generate_random_date(starting_date, due_date)
            else:
                returned_date = self.generate_random_date(starting_date, date.today())
            self.rental_repo.add(Rental(i, movie, client, starting_date, due_date, returned_date))
        # to test late rentals visually
        # self.rental_repo.add(Rental(11, 1, 1, date(2020, 11, 24), date(2020, 11, 25)))

    def generate_most_rented_movies(self):
        """
        Generates a list containing the most rented movies in decreasing order of the days they were rented
        :return: The list of the most rented movies and the number of days they were rented
        """
        sorted_movies = []
        movies_dict = {}
        for rental in self.get_current_list():
            if rental.movie_id not in movies_dict:
                movies_dict[rental.movie_id] = 0
            if rental.returned_date is None:
                movies_dict[rental.movie_id] += (date.today() - rental.rented_date).days
            else:
                movies_dict[rental.movie_id] += (rental.returned_date - rental.rented_date).days
        for entry in movies_dict:
            sorted_movies.append(MoviesRentedDays(entry, self.get_movie_title(entry), movies_dict[entry]))
        IterableStructure.sort(sorted_movies, lambda x, y: x.days > y.days)
        return sorted_movies

    def generate_most_active_clients(self):
        """
        Generates a list containing the most active clients in decreasing order of the days they rented a movie
        :return: The list of the most active clients and the number of days they rented something
        """
        sorted_clients = []
        clients_dict = {}
        for rental in self.get_current_list():
            if rental.client_id not in clients_dict:
                clients_dict[rental.client_id] = 0
            if rental.returned_date is None:
                clients_dict[rental.client_id] += (date.today() - rental.rented_date).days
            else:
                clients_dict[rental.client_id] += (rental.returned_date - rental.rented_date).days
        for entry in clients_dict:
            sorted_clients.append(ClientRentedDays(entry, self.get_client_name(entry), clients_dict[entry]))
        IterableStructure.sort(sorted_clients, lambda x, y: x.days > y.days)
        return sorted_clients

    def generate_late_rentals(self):
        """
        Generates a list containing the overdue movies in decreasing order of overdue days
        :return: The list of overdue movies and the number of days they are overdue
        """
        sorted_rentals = []
        rental_dict = {}
        for rental in self.get_current_list():
            if rental.returned_date is None:
                rental_dict[rental.id] = (date.today() - rental.due_date).days
        for entry in rental_dict:
            movie_title = self.get_movie_title_from_rental_with_id(entry)
            sorted_rentals.append(RentalRentedDays(entry, movie_title, rental_dict[entry]))
        IterableStructure.sort(sorted_rentals, lambda x, y: x.days > y.days)
        return sorted_rentals
