from datetime import date


class ShopException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

    def __str__(self):
        return super().__str__()


class InvalidDateException(ShopException):
    def __init__(self, msg):
        super().__init__(msg)


class InvalidOptionException(ShopException):
    def __init__(self, msg):
        super().__init__(msg)


class ClientException(ShopException):
    def __init__(self, msg):
        super().__init__(msg)


class MovieException(ShopException):
    def __init__(self, msg):
        super().__init__(msg)


class RentalException(ShopException):
    def __init__(self, msg):
        super().__init__(msg)


class LateClientException(RentalException):
    def __init__(self, msg):
        super().__init__(msg)


class RentedMovieException(RentalException):
    def __init__(self, msg):
        super().__init__(msg)


class UndoRedoException(ShopException):
    def __init__(self, msg):
        super().__init__(msg)


class SettingsException(ShopException):
    def __init__(self, msg):
        super().__init__(msg)


class ClientValidator:

    @staticmethod
    def validate(client):
        """
        Checks if a given client is valid
        :param client: The client
        :return: nothing
        Raise ClientException if the client is not valid:
         - its ID is not a positive integer
         - its name is not a string
        """
        if not isinstance(client.id, int):
            raise ClientException("Invalid Client! The ID must be an integer!")
        if client.id < 1:
            raise ClientException("Invalid Client! The ID must be positive!")
        if not isinstance(client.name, str):
            raise ClientException("Invalid Client! The name must be a string!")


class MovieValidator:

    @staticmethod
    def validate(movie):
        """
        Checks if a given movie is valid
        :param movie: The movie
        :return: nothing
        Raise MovieException if the movie is not valid:
         - its ID is not a positive integer
         - its title is not a string
         - its genre is not a string
         - its description is not a string
        """
        if not isinstance(movie.id, int):
            raise MovieException("Invalid Movie! The ID must be an integer!")
        if movie.id < 1:
            raise MovieException("Invalid Movie! The ID must be positive!")
        if not isinstance(movie.title, str):
            raise MovieException("Invalid Movie! The title must be a string!")
        if not isinstance(movie.genre, str):
            raise MovieException("Invalid Movie! The genre must be a string!")
        if not isinstance(movie.description, str):
            raise MovieException("Invalid Movie! The description must be a string!")


class RentalValidator:

    @staticmethod
    def validate(rental):
        """
        Checks if a given rental is valid
        :param rental: The rental
        :return: nothing
        Raise RentalException if the rental is not valid:
         - its ID is not a positive integer
         - the clients ID is not a positive integer
         - the movies ID is not a positive integer
         - the rental date is not a date
         - the due date is not a date bigger than the rental date
         - the return date is not None or a date bigger than the rental date
        """
        if not isinstance(rental.id, int):
            raise RentalException("Invalid Rental! The ID must be an integer!")
        if rental.id < 1:
            raise RentalException("Invalid Rental! The ID must be positive!")
        if not isinstance(rental.movie_id, int):
            raise RentalException("Invalid Rental! The movie's ID must be an integer!")
        if rental.movie_id < 1:
            raise RentalException("Invalid Rental! The movie's ID must be positive!")
        if not isinstance(rental.client_id, int):
            raise RentalException("Invalid Rental! The client's ID must be an integer!")
        if rental.client_id < 1:
            raise RentalException("Invalid Rental! The client's ID must be positive!")
        if not isinstance(rental.rented_date, date):
            raise RentalException("Invalid Rental! The rental date must be a date!")
        if not isinstance(rental.due_date, date):
            raise RentalException("Invalid Rental! The due date must be a date!")
        if rental.returned_date is not None and not isinstance(rental.returned_date, date):
            raise RentalException("Invalid Rental! The returned date must be a date or None!")
        if rental.rented_date > rental.due_date:
            raise RentalException("Invalid Rental! The rental date cannot be bigger than the due date!")
        if rental.returned_date is not None and rental.returned_date < rental.rented_date:
            raise RentalException("Invalid Rental! The rental date cannot be bigger than the returned date!")
