class MoviesRentedDays:
    def __init__(self, movie_id, movie_title, days):
        """
        Generates a MoviesRentedDays DTO
        :param movie_id: The ID of the movie
        :param movie_title: The title of the movie
        :param days: The number of days the movie was rented
        """
        self.__movie_id = movie_id
        self.__movie_title = movie_title
        self.__days = days

    @property
    def movie_id(self):
        return self.__movie_id

    @property
    def movie_title(self):
        return self.__movie_title

    @property
    def days(self):
        return self.__days

    def __str__(self):
        return "Movie ID: {0}\nTitle: {1}\nDays rented: {2}\n".format(self.movie_id, self.movie_title, self.days)


class ClientRentedDays:
    def __init__(self, client_id, client_name, days):
        """
        Generates a ClientRentedDays object
        :param client_id: The ID of the client
        :param client_name: The client's name
        :param days: The number of days in which the client had something rented
        """
        self.__client_id = client_id
        self.__client_name = client_name
        self.__days = days

    @property
    def client_id(self):
        return self.__client_id

    @property
    def client_name(self):
        return self.__client_name

    @property
    def days(self):
        return self.__days

    def __str__(self):
        return "Client ID: {0}\nName: {1}\nMovie rental days: {2}".format(self.client_id, self.client_name, self.days)


class RentalRentedDays:
    def __init__(self, rental_id, movie_title, days):
        """
        Generates a RentalRentedDays object
        :param rental_id: The rental's ID
        :param movie_title: The title of the movie that was rented
        :param days: The number of overdue days for the rental
        """
        self.__rental_id = rental_id
        self.__movie_title = movie_title
        self.__days = days

    @property
    def rental_id(self):
        return self.__rental_id

    @property
    def movie_title(self):
        return self.__movie_title

    @property
    def days(self):
        return self.__days

    def __str__(self):
        return "Rental ID: {0}\nMovie title: {1}\nOverdue days: {2}".format(self.rental_id, self.movie_title, self.days)
