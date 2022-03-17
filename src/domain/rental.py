class Rental:

    def __init__(self, rental_id, movie_id, client_id, rented_date, due_date, returned_date=None):
        """
        Creates a new rental
        :param rental_id: The rental's ID
        :param movie_id: The rented movie's ID
        :param client_id: The renting client's ID
        :param rented_date: The rental's date
        :param due_date: The rental's due date
        :param returned_date: The date in which the movie was returned, or, if the movie wasn't returned, None
        """
        self.__rental_id = rental_id
        self.__movie_id = movie_id
        self.__client_id = client_id
        self.__rented_date = rented_date
        self.__due_date = due_date
        self.__returned_date = returned_date

    @property
    def id(self):
        return self.__rental_id

    @property
    def movie_id(self):
        return self.__movie_id

    @property
    def client_id(self):
        return self.__client_id

    @property
    def rented_date(self):
        return self.__rented_date

    @property
    def due_date(self):
        return self.__due_date

    @property
    def returned_date(self):
        return self.__returned_date

    @returned_date.setter
    def returned_date(self, value):
        self.__returned_date = value

    def __str__(self):
        string = "-" * 10 + " ID: " + str(self.id) + " " + "-" * 10 + "\n"
        string += "Movie ID: {0}\nClient ID: {1}\nRented Date: {2}\nDue Date: {3}\nReturned Date: ". \
            format(self.movie_id, self.client_id, self.rented_date, self.due_date)
        return string + "Not Returned" if self.returned_date is None else string + str(self.returned_date)
