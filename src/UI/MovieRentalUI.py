from datetime import date

from domain.colors import F_WHITE_B, RESET, F_CYAN, F_GREEN, F_RED, F_YELLOW
from domain.validators import ShopException, InvalidDateException, InvalidOptionException, ClientException, \
    MovieException
from services.handlers import UndoHandlers, RedoHandlers
from services.undoredo import FunctionCall, UndoRedoOperation


class MovieRentalUI:
    def __init__(self, client_service, movie_service, rental_service, operation_manager):
        self.__client_service = client_service
        self.__movie_service = movie_service
        self.__rental_service = rental_service
        self.__operation_manager = operation_manager

    @property
    def client_service(self):
        return self.__client_service

    @property
    def movie_service(self):
        return self.__movie_service

    @property
    def rental_service(self):
        return self.__rental_service

    @staticmethod
    def separate_date(date_string):
        date_numbers = date_string.split("/")
        if len(date_numbers) != 3:
            raise InvalidDateException("Invalid date! It doesn't have 3 fields!")
        if len(date_numbers[0]) != 2 and len(date_numbers[1]) != 2 and len(date_numbers[2]) != 4:
            raise InvalidDateException("Invalid date! It doesn't follow the format!")
        date_numbers.reverse()
        return [int(number) for number in date_numbers]

    @staticmethod
    def print_unordered_list_of_elements(element_list):
        for element in element_list:
            print(RESET + F_YELLOW + str(element))
            print()

    @staticmethod
    def print_ordered_list_of_elements(element_list):
        for i in range(len(element_list)):
            text = RESET + F_CYAN + "-" * 10 + " " + str(i + 1)
            if i % 10 == 0 and i % 100 != 10:
                text += "st "
            elif i % 10 == 1 and i % 100 != 11:
                text += "nd "
            elif i % 10 == 2 and i % 100 != 12:
                text += "rd "
            else:
                text += "th "
            text += "-" * 10
            print(text)
            print(RESET + F_YELLOW + str(element_list[i]))
            print()

    def add_client_menu(self):
        client_id = input("Give the client's ID: ")
        name = input("Give the client's name: ")
        try:
            client_id = int(client_id)
        except ValueError:
            raise ValueError("Invalid ID! It must be an integer!")
        self.client_service.add(client_id, name)
        undo_call = FunctionCall(self.client_service, UndoHandlers.ADD_CLIENT, (client_id,))
        redo_call = FunctionCall(self.client_service, RedoHandlers.ADD_CLIENT, (client_id, name))
        self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))

    def remove_client_menu(self):
        client_id = input("Give the client's ID: ")
        try:
            client_id = int(client_id)
        except ValueError:
            raise ValueError("Invalid ID! It must be an integer!")
        removed_things = self.client_service.remove(client_id)
        undo_call = FunctionCall(self.client_service, UndoHandlers.REMOVE_CLIENT, removed_things)
        redo_call = FunctionCall(self.client_service, RedoHandlers.REMOVE_CLIENT, (client_id,))
        self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))

    def update_client_menu(self):
        client_id = input("Give the client's ID: ")
        new_name = input("Give the client's new name: ")
        try:
            client_id = int(client_id)
        except ValueError:
            raise ValueError("Invalid ID! It must be an integer!")
        old_client_attributes = self.client_service.update(client_id, new_name)
        undo_call = FunctionCall(self.client_service, UndoHandlers.UPDATE_CLIENT, old_client_attributes)
        redo_call = FunctionCall(self.client_service, RedoHandlers.UPDATE_CLIENT, (client_id, new_name))
        self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))

    def list_client_menu(self):
        self.print_unordered_list_of_elements(self.client_service.get_current_list())

    def add_movie_menu(self):
        movie_id = input("Give the movie's ID: ")
        title = input("Give the movie's title: ")
        description = input("Give the movie's description: ")
        genre = input("Give the movie's genre: ")
        try:
            movie_id = int(movie_id)
        except ValueError:
            raise ValueError("Invalid ID! It must be an integer!")
        self.movie_service.add(movie_id, title, description, genre)
        undo_call = FunctionCall(self.movie_service, UndoHandlers.ADD_MOVIE, (movie_id,))
        redo_call = FunctionCall(self.movie_service, RedoHandlers.ADD_MOVIE, (movie_id, title, description, genre))
        self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))

    def remove_movie_menu(self):
        movie_id = input("Give the movie's ID: ")
        try:
            movie_id = int(movie_id)
        except ValueError:
            raise ValueError("Invalid ID! It must be an integer!")
        removed_things = self.movie_service.remove(movie_id)
        undo_call = FunctionCall(self.movie_service, UndoHandlers.REMOVE_MOVIE, removed_things)
        redo_call = FunctionCall(self.movie_service, RedoHandlers.REMOVE_MOVIE, (movie_id,))
        self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))

    def update_movie_menu(self):
        movie_id = input("Give the movie's ID: ")
        new_title = input("Give the movie's new title: ")
        new_description = input("Give the movie's new description: ")
        new_genre = input("Give the movie's new genre: ")
        try:
            movie_id = int(movie_id)
        except ValueError:
            raise ValueError("Invalid ID! It must be an integer!")
        old_movie_attributes = self.movie_service.update(movie_id, new_title, new_description, new_genre)
        undo_call = FunctionCall(self.movie_service, UndoHandlers.UPDATE_MOVIE, old_movie_attributes)
        redo_call = FunctionCall(self.movie_service, RedoHandlers.UPDATE_MOVIE, (movie_id, new_title, new_description,
                                                                                 new_genre))
        self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))

    def list_movie_menu(self):
        self.print_unordered_list_of_elements(self.movie_service.get_current_list())

    def rent_movie_menu(self):
        rental_id = input("Give the rental's ID: ")
        movie_id = input("Give the movie's ID: ")
        client_id = input("Give the client's ID: ")
        rental_date = input("Give the rental date (in the format DD/MM/YYYY): ")
        due_date = input("Give the due date (in the format DD/MM/YYYY): ")
        try:
            rental_id = int(rental_id)
            movie_id = int(movie_id)
            client_id = int(client_id)
        except ValueError:
            raise ValueError("Invalid IDs! They must be integers!")
        rental_date = date(*self.separate_date(rental_date))
        due_date = date(*self.separate_date(due_date))
        self.rental_service.add_rental(rental_id, movie_id, client_id, rental_date, due_date)
        undo_call = FunctionCall(self.rental_service, UndoHandlers.RENT_MOVIE, (rental_id,))
        redo_call = FunctionCall(self.rental_service, RedoHandlers.RENT_MOVIE, (rental_id, movie_id, client_id,
                                                                                rental_date, due_date))
        self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))

    def return_movie_menu(self):
        rental_id = input("Give the rental's ID: ")
        try:
            rental_id = int(rental_id)
        except ValueError:
            raise ValueError("Invalid ID! It must be an integer!")
        return_date = input("Give the date of the return (in the format DD/MM/YYYY): ")
        return_date = date(*self.separate_date(return_date))
        self.rental_service.return_movie(rental_id, return_date)
        undo_call = FunctionCall(self.rental_service, UndoHandlers.RETURN_MOVIE, (rental_id,))
        redo_call = FunctionCall(self.rental_service, RedoHandlers.RETURN_MOVIE, (rental_id, return_date))
        self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))

    def list_rentals_menu(self):
        self.print_unordered_list_of_elements(self.rental_service.get_current_list())

    def search_client_menu(self):
        options_list = {"1": "id", "2": "name"}
        print("Search by:\n"
              "1. The Client's ID\n"
              "2. The Client's name\n"
              "3. Every field.")
        option = input("Choose an option: ")
        if option not in ["1", "2", "3"]:
            raise InvalidOptionException("The option does not exist!")
        searching_input = input("Search for :").strip().lower()
        if option == "3":
            searched_list = self.client_service.search_for_clients_by_everything(searching_input)
        else:
            searched_list = self.client_service.search_for_clients_by_attribute(searching_input, options_list[option])
        if len(searched_list) == 0:
            raise ClientException("There are no clients that fit that criteria!")
        self.print_unordered_list_of_elements(searched_list)

    def search_movie_menu(self):
        options_list = {"1": "id", "2": "title", "3": "description", "4": "genre"}
        print("Search by:\n"
              "1. The Movie's ID\n"
              "2. The Movie's title\n"
              "3. The Movie's description\n"
              "4. The Movie's genre\n"
              "5. Every field.")
        option = input("Choose an option: ")
        if option not in ["1", "2", "3", "4", "5"]:
            raise InvalidOptionException("The option does not exist!")
        searching_input = input("Search for:").strip().lower()
        if option == "5":
            searched_list = self.movie_service.search_for_movies_by_everything(searching_input)
        else:
            searched_list = self.movie_service.search_for_movies_by_attribute(searching_input, options_list[option])
        if len(searched_list) == 0:
            raise MovieException("There are no movies that fit that criteria!")
        self.print_unordered_list_of_elements(searched_list)

    def most_rented_movies_menu(self):
        most_rented_movies = self.rental_service.generate_most_rented_movies()
        if len(most_rented_movies) == 0:
            raise MovieException("No movies have been rented!")
        self.print_ordered_list_of_elements(most_rented_movies)

    def most_active_clients_menu(self):
        most_active_clients = self.rental_service.generate_most_active_clients()
        if len(most_active_clients) == 0:
            raise ClientException("No client has rented anything!")
        self.print_ordered_list_of_elements(most_active_clients)

    def late_rentals_menu(self):
        late_rentals = self.rental_service.generate_late_rentals()
        if len(late_rentals) == 0:
            raise MovieException("There are no late rentals!")
        self.print_ordered_list_of_elements(late_rentals)

    def undo_menu(self):
        self.__operation_manager.undo()

    def redo_menu(self):
        self.__operation_manager.redo()

    @staticmethod
    def print_menu():
        print(RESET + F_WHITE_B +
              "1. Add a new client\n"
              "2. Remove a client\n"
              "3. Update a client\n"
              "4. List all clients\n"
              "5. Add a new movie\n"
              "6. Remove a movie\n"
              "7. Update a movie\n"
              "8. List all movies\n"
              "9. Rent a movie\n"
              "10. Return a movie\n"
              "11. List all rentals\n"
              "12. Search for clients\n"
              "13. Search for movies\n"
              "14. List most rented movies\n"
              "15. List most active clients\n"
              "16. List overdue movies\n"
              "17. Undo last operation\n"
              "18. Redo last operation\n"
              "19. Exit the application\n")

    def run_menu(self):
        options_dictionary = {"1": self.add_client_menu, "2": self.remove_client_menu, "3": self.update_client_menu,
                              "4": self.list_client_menu, "5": self.add_movie_menu, "6": self.remove_movie_menu,
                              "7": self.update_movie_menu, "8": self.list_movie_menu, "9": self.rent_movie_menu,
                              "10": self.return_movie_menu, "11": self.list_rentals_menu, "12": self.search_client_menu,
                              "13": self.search_movie_menu, "14": self.most_rented_movies_menu,
                              "15": self.most_active_clients_menu, "16": self.late_rentals_menu, "17": self.undo_menu,
                              "18": self.redo_menu}
        self.print_menu()
        option = input("Choose an option: ")
        try:
            print(RESET + F_GREEN)
            if option == "19":
                return True
            if option not in options_dictionary.keys():
                raise InvalidOptionException("Invalid Option!")
            options_dictionary[option]()
            return False
        except ShopException as se:
            print(RESET + F_RED + str(se), "\n")
        except ValueError as ve:
            print(RESET + F_RED + str(ve), "\n")
