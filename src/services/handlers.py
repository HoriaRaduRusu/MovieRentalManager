from enum import Enum


class Handlers:

    @staticmethod
    def remove_client_handler(client_service, client_id):
        """
        Handles the remove client method for the undo and redo functionalities
        :param client_service: The object that removes the client
        :param client_id: The ID of the client to be removed
        :return: nothing
        """
        client_service.remove(client_id)

    @staticmethod
    def add_client_handler(client_service, client_id, client_name):
        """
        Handles the add client method for the undo and redo functionalities
        :param client_service: The object that adds the client
        :param client_id: The ID of the client to be added
        :param client_name: The name of the client to be added
        :return: nothing
        """
        client_service.add(client_id, client_name)

    @staticmethod
    def add_client_and_rentals_handler(client_service, client_id, client_name, rentals):
        """
        Handles the add client and rentals method for the undo and redo functionalities
        :param client_service: The object that adds the client and rentals
        :param client_id: The ID of the client to be added
        :param client_name: The name of the client to be added
        :param rentals: The rentals to be added
        :return: nothing
        """
        client_service.add_client_and_rentals(client_id, client_name, rentals)

    @staticmethod
    def update_client_handler(client_service, client_id, client_name):
        """
        Handles the update client method for the undo and redo functionalities
        :param client_service: The object that updates the client
        :param client_id: The ID of the client to be updated
        :param client_name: The new name of the updated client
        :return: nothing
        """
        client_service.update(client_id, client_name)

    @staticmethod
    def remove_movie_handler(movie_service, movie_id):
        """
        Handles the remove movie method for the undo and redo functionalities
        :param movie_service: The object that removes the movie
        :param movie_id: The ID of the movie to be removed
        :return: nothing
        """
        movie_service.remove(movie_id)

    @staticmethod
    def add_movie_handler(movie_service, movie_id, movie_title, movie_description, movie_genre):
        """
        Handles the add movie method for the undo and redo functionalities
        :param movie_service: The object that adds the movie
        :param movie_id: The ID of the movie to be added
        :param movie_title: The title of the movie to be added
        :param movie_description: The description of the movie to be added
        :param movie_genre: The genre of the movie to be added
        :return: nothing
        """
        movie_service.add(movie_id, movie_title, movie_description, movie_genre)

    @staticmethod
    def add_movie_and_rentals_handler(movie_service, movie_id, movie_title, movie_description, movie_genre, rentals):
        """
        Handles the add movie and rentals method for the undo and redo functionalities
        :param movie_service: The object that adds the movie and rentals
        :param movie_id: The ID of the movie to be added
        :param movie_title: The title of the movie to be added
        :param movie_description: The description of the movie to be added
        :param movie_genre: The genre of the movie to be added
        :param rentals: The list of rentals to be added
        :return: nothing
        """
        movie_service.add_movie_and_rentals(movie_id, movie_title, movie_description, movie_genre, rentals)

    @staticmethod
    def update_movie_handler(movie_service, movie_id, movie_title, movie_description, movie_genre):
        """
        Handles the update movie method for the undo and redo functionalities
        :param movie_service: The object that updates the movie
        :param movie_id: The ID of the movie to be updated
        :param movie_title: The new title of the updated movie
        :param movie_description: The new description of the updated movie
        :param movie_genre: The new genre of the updated movie
        :return: nothing
        """
        movie_service.update(movie_id, movie_title, movie_description, movie_genre)

    @staticmethod
    def delete_rental_handler(rental_service, rental_id):
        """
        Handles the delete rental method for the undo and redo functionalities
        :param rental_service: The object that deletes the rental
        :param rental_id: The ID of the rental to be added
        :return: nothing
        """
        rental_service.delete_rental(rental_id)

    @staticmethod
    def cancel_return_handler(rental_service, rental_id):
        """
        Handles the cancel return method for the undo and redo functionalities
        :param rental_service: The object that cancels the return
        :param rental_id: The ID of the rental that will have the return canceled
        :return: nothing
        """
        rental_service.cancel_return(rental_id)

    @staticmethod
    def add_rental_handler(rental_service, rental_id, movie_id, client_id, rented_date, due_date):
        """
        Handles the add rental method for the undo and redo functionalities
        :param rental_service: The object that adds the rental
        :param rental_id: The ID of the rental to be added
        :param movie_id: The movie ID of the rental to be added
        :param client_id: The client ID of the rental to be added
        :param rented_date: The rented date of the rental to be added
        :param due_date: The due date of the rental to be added
        :return: nothing
        """
        rental_service.add_rental(rental_id, movie_id, client_id, rented_date, due_date)

    @staticmethod
    def return_movie_handler(rental_service, rental_id, return_date):
        """
        Handles the return movie method for the undo and redo functionalities
        :param rental_service: The object that returns a movie
        :param rental_id: The ID of the rental to be returned
        :param return_date: The date of the return
        :return: nothing
        """
        rental_service.return_movie(rental_id, return_date)


class UndoHandlers(Enum):
    ADD_CLIENT = Handlers.remove_client_handler
    REMOVE_CLIENT = Handlers.add_client_and_rentals_handler
    UPDATE_CLIENT = Handlers.update_client_handler

    ADD_MOVIE = Handlers.remove_movie_handler
    REMOVE_MOVIE = Handlers.add_movie_and_rentals_handler
    UPDATE_MOVIE = Handlers.update_movie_handler

    RENT_MOVIE = Handlers.delete_rental_handler
    RETURN_MOVIE = Handlers.cancel_return_handler


class RedoHandlers(Enum):
    ADD_CLIENT = Handlers.add_client_handler
    REMOVE_CLIENT = Handlers.remove_client_handler
    UPDATE_CLIENT = Handlers.update_client_handler

    ADD_MOVIE = Handlers.add_movie_handler
    REMOVE_MOVIE = Handlers.remove_movie_handler
    UPDATE_MOVIE = Handlers.update_movie_handler

    RENT_MOVIE = Handlers.add_rental_handler
    RETURN_MOVIE = Handlers.return_movie_handler
