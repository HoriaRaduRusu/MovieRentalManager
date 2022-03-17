import tkinter
from datetime import date

from domain.validators import ShopException, InvalidDateException
from services.handlers import UndoHandlers, RedoHandlers
from services.undoredo import FunctionCall, UndoRedoOperation


class DataException(ShopException):
    def __init__(self, msg):
        super().__init__(msg)


class LabelEntry(tkinter.Frame):
    def __init__(self, parent, label, entry_width=25):
        tkinter.Frame.__init__(self, parent)

        self.label = tkinter.Label(master=self, text=label)
        self.entry = tkinter.Entry(master=self, width=entry_width)

        self.label.pack(side=tkinter.LEFT)
        self.entry.pack(side=tkinter.LEFT)

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, tkinter.END)


class MovieRentalGUI:
    def __init__(self, client_service, movie_service, rental_service, operation_manager):
        self.__client_service = client_service
        self.__movie_service = movie_service
        self.__rental_service = rental_service
        self.__operation_manager = operation_manager
        self._run_menu()

    @staticmethod
    def separate_date(date_string):
        date_numbers = date_string.split("/")
        if len(date_numbers) != 3:
            raise InvalidDateException("Invalid date! It doesn't have 3 fields!")
        if len(date_numbers[0]) != 2 and len(date_numbers[1]) != 2 and len(date_numbers[2]) != 4:
            raise InvalidDateException("Invalid date! It doesn't follow the format!")
        date_numbers.reverse()
        return [int(number) for number in date_numbers]

    def clear_result_box(self):
        self._result_box["state"] = "normal"
        self._result_box.delete(1.0, tkinter.END)
        self._result_box["state"] = "disabled"

    def print_line_to_result_box(self, line):
        self._result_box["state"] = "normal"
        self._result_box.insert(tkinter.END, line)
        self._result_box["state"] = "disabled"

    def print_unordered_list_to_result_box(self, unordered_list):
        for elem in unordered_list:
            self.print_line_to_result_box(str(elem) + "\n")

    def print_ordered_list_to_result_box(self, element_list):
        for i in range(len(element_list)):
            text = "-" * 10 + " " + str(i + 1)
            if i % 10 == 0 and i % 100 != 10:
                text += "st "
            elif i % 10 == 1 and i % 100 != 11:
                text += "nd "
            elif i % 10 == 2 and i % 100 != 12:
                text += "rd "
            else:
                text += "th "
            text += "-" * 10
            self.print_line_to_result_box(text + "\n")
            self.print_line_to_result_box(str(element_list[i]) + "\n")

    def clear_inputs(self):
        self._lbl_with_ent_client_id.clear()
        self._lbl_with_ent_client_name.clear()
        self._lbl_with_ent_client_search.clear()
        self._lbl_with_ent_movie_id.clear()
        self._lbl_with_ent_movie_title.clear()
        self._lbl_with_ent_movie_description.clear()
        self._lbl_with_ent_movie_genre.clear()
        self._lbl_with_ent_movie_search.clear()
        self._lbl_with_ent_rental_id.clear()
        self._lbl_with_ent_rental_movie_id.clear()
        self._lbl_with_ent_rental_client_id.clear()
        self._lbl_with_ent_rental_date.clear()
        self._lbl_with_ent_rental_due_date.clear()
        self._lbl_with_ent_rental_return_date.clear()

    def add_client(self):
        client_id = self._lbl_with_ent_client_id.get()
        name = self._lbl_with_ent_client_name.get()
        self.clear_result_box()
        self.clear_inputs()
        try:
            if client_id == "" or name == "":
                raise DataException("Missing argument!")
            try:
                client_id = int(client_id)
            except ValueError:
                raise DataException("The ID must be an integer!")
            self.__client_service.add(client_id, name)
            undo_call = FunctionCall(self.__client_service, UndoHandlers.ADD_CLIENT, (client_id,))
            redo_call = FunctionCall(self.__client_service, RedoHandlers.ADD_CLIENT, (client_id, name))
            self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_line_to_result_box("The client was added successfully!")

    def delete_client(self):
        client_id = self._lbl_with_ent_client_id.get()
        self.clear_result_box()
        self.clear_inputs()
        try:
            if client_id == "":
                raise DataException("Missing argument!")
            try:
                client_id = int(client_id)
            except ValueError:
                raise DataException("Invalid ID! It must be an integer!")
            removed_things = self.__client_service.remove(client_id)
            undo_call = FunctionCall(self.__client_service, UndoHandlers.REMOVE_CLIENT, removed_things)
            redo_call = FunctionCall(self.__client_service, RedoHandlers.REMOVE_CLIENT, (client_id,))
            self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_line_to_result_box("The client was removed successfully!")

    def list_clients(self):
        self.clear_result_box()
        self.clear_inputs()
        self.print_unordered_list_to_result_box(self.__client_service.get_current_list())

    def update_client(self):
        client_id = self._lbl_with_ent_client_id.get()
        new_name = self._lbl_with_ent_client_name.get()
        self.clear_result_box()
        self.clear_inputs()
        try:
            if client_id == "" or new_name == "":
                raise DataException("Missing argument!")
            try:
                client_id = int(client_id)
            except ValueError:
                raise DataException("Invalid ID! It must be an integer!")
            old_client_attributes = self.__client_service.update(client_id, new_name)
            undo_call = FunctionCall(self.__client_service, UndoHandlers.UPDATE_CLIENT, old_client_attributes)
            redo_call = FunctionCall(self.__client_service, RedoHandlers.UPDATE_CLIENT, (client_id, new_name))
            self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_line_to_result_box("The client was updated successfully!")

    def search_client(self):
        client_id = self._lbl_with_ent_client_id.get().strip().lower()
        name = self._lbl_with_ent_client_name.get().strip().lower()
        everything = self._lbl_with_ent_client_search.get().strip().lower()
        self.clear_result_box()
        self.clear_inputs()
        searching_list = [client_id, name, everything]
        try:
            if searching_list.count("") < 2:
                raise DataException("You cannot search by more than one field!")
            elif searching_list.count("") == 3:
                raise DataException("No searching input was given!")
            if everything != "":
                searched_list = self.__client_service.search_for_clients_by_everything(everything)
            elif client_id != "":
                searched_list = self.__client_service.search_for_clients_by_attribute(client_id, "id")
            else:
                searched_list = self.__client_service.search_for_clients_by_attribute(name, "name")
            if len(searched_list) == 0:
                raise DataException("There are no clients that fit that criteria!")
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_unordered_list_to_result_box(searched_list)

    def add_movie(self):
        movie_id = self._lbl_with_ent_movie_id.get()
        title = self._lbl_with_ent_movie_title.get()
        description = self._lbl_with_ent_movie_description.get()
        genre = self._lbl_with_ent_movie_genre.get()
        self.clear_result_box()
        self.clear_inputs()
        attribute_list = [movie_id, title, description, genre]
        try:
            if "" in attribute_list:
                raise DataException("Missing arguments!")
            try:
                movie_id = int(movie_id)
            except ValueError:
                raise DataException("Invalid ID! It must be an integer!")
            self.__movie_service.add(movie_id, title, description, genre)
            undo_call = FunctionCall(self.__movie_service, UndoHandlers.ADD_MOVIE, (movie_id,))
            redo_call = FunctionCall(self.__movie_service, RedoHandlers.ADD_MOVIE, (movie_id, title, description,
                                                                                    genre))
            self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_line_to_result_box("The movie was added successfully!")

    def delete_movie(self):
        movie_id = self._lbl_with_ent_movie_id.get()
        self.clear_result_box()
        self.clear_inputs()
        try:
            if movie_id == "":
                raise DataException("Missing arguments!")
            try:
                movie_id = int(movie_id)
            except ValueError:
                raise DataException("Invalid ID! It must be an integer!")
            removed_things = self.__movie_service.remove(movie_id)
            undo_call = FunctionCall(self.__movie_service, UndoHandlers.REMOVE_MOVIE, removed_things)
            redo_call = FunctionCall(self.__movie_service, RedoHandlers.REMOVE_MOVIE, (movie_id,))
            self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_line_to_result_box("The movie was removed successfully!")

    def list_movies(self):
        self.clear_result_box()
        self.clear_inputs()
        self.print_unordered_list_to_result_box(self.__movie_service.get_current_list())

    def update_movie(self):
        movie_id = self._lbl_with_ent_movie_id.get()
        new_title = self._lbl_with_ent_movie_title.get()
        new_description = self._lbl_with_ent_movie_description.get()
        new_genre = self._lbl_with_ent_movie_genre.get()
        self.clear_result_box()
        self.clear_inputs()
        attributes = [movie_id, new_title, new_description, new_genre]
        try:
            if "" in attributes:
                raise DataException("Missing arguments!")
            try:
                movie_id = int(movie_id)
            except ValueError:
                raise DataException("Invalid ID! It must be an integer!")
            old_movie_attributes = self.__movie_service.update(movie_id, new_title, new_description, new_genre)
            undo_call = FunctionCall(self.__movie_service, UndoHandlers.UPDATE_MOVIE, old_movie_attributes)
            redo_call = FunctionCall(self.__movie_service, RedoHandlers.UPDATE_MOVIE, (movie_id, new_title,
                                                                                       new_description, new_genre))
            self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_line_to_result_box("The movie was updated successfully!")

    def search_movie(self):
        movie_id = self._lbl_with_ent_movie_id.get().strip().lower()
        title = self._lbl_with_ent_movie_title.get().strip().lower()
        description = self._lbl_with_ent_movie_description.get().strip().lower()
        genre = self._lbl_with_ent_movie_genre.get().strip().lower()
        everything = self._lbl_with_ent_movie_search.get().strip().lower()
        self.clear_result_box()
        self.clear_inputs()
        searching_list = [movie_id, title, description, genre, everything]
        try:
            if searching_list.count("") < 4:
                raise DataException("You cannot search by more than one field!")
            elif searching_list.count("") == 5:
                raise DataException("No searching input was given!")
            if everything != "":
                searched_list = self.__movie_service.search_for_movies_by_everything(everything)
            elif movie_id != "":
                searched_list = self.__movie_service.search_for_movies_by_attribute(movie_id, "id")
            elif title != "":
                searched_list = self.__movie_service.search_for_movies_by_attribute(title, "title")
            elif description != "":
                searched_list = self.__movie_service.search_for_movies_by_attribute(description, "description")
            else:
                searched_list = self.__movie_service.search_for_movies_by_attribute(genre, "genre")
            if len(searched_list) == 0:
                raise DataException("There are no movies that fit that criteria!")
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_unordered_list_to_result_box(searched_list)

    def rent_movie(self):
        rental_id = self._lbl_with_ent_rental_id.get()
        movie_id = self._lbl_with_ent_rental_movie_id.get()
        client_id = self._lbl_with_ent_rental_client_id.get()
        rental_date = self._lbl_with_ent_rental_date.get()
        due_date = self._lbl_with_ent_rental_due_date.get()
        self.clear_result_box()
        self.clear_inputs()
        attributes = [rental_id, movie_id, client_id, rental_date, due_date]
        try:
            if "" in attributes:
                raise DataException("Missing arguments!")
            try:
                rental_id = int(rental_id)
                movie_id = int(movie_id)
                client_id = int(client_id)
            except ValueError:
                raise DataException("Invalid IDs! They must be integers!")
            try:
                rental_date = date(*self.separate_date(rental_date))
                due_date = date(*self.separate_date(due_date))
            except ValueError:
                raise DataException("Invalid dates!")
            self.__rental_service.add_rental(rental_id, movie_id, client_id, rental_date, due_date)
            undo_call = FunctionCall(self.__rental_service, UndoHandlers.RENT_MOVIE, (rental_id,))
            redo_call = FunctionCall(self.__rental_service, RedoHandlers.RENT_MOVIE, (rental_id, movie_id, client_id,
                                                                                      rental_date, due_date))
            self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_line_to_result_box("The rental was successful!")

    def return_movie(self):
        rental_id = self._lbl_with_ent_rental_id.get()
        return_date = self._lbl_with_ent_rental_return_date.get()
        self.clear_result_box()
        self.clear_inputs()
        try:
            if rental_id == "" or return_date == "":
                raise DataException("Missing arguments!")
            try:
                rental_id = int(rental_id)
            except ValueError:
                raise DataException("Invalid ID! It must be an integer!")
            try:
                return_date = date(*self.separate_date(return_date))
            except ValueError:
                raise DataException("Invalid date!")
            self.__rental_service.return_movie(rental_id, return_date)
            undo_call = FunctionCall(self.__rental_service, UndoHandlers.RETURN_MOVIE, (rental_id,))
            redo_call = FunctionCall(self.__rental_service, RedoHandlers.RETURN_MOVIE, (rental_id, return_date))
            self.__operation_manager.record_operation(UndoRedoOperation(undo_call, redo_call))
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_line_to_result_box("The rental was returned successfully!")

    def list_rentals(self):
        self.clear_result_box()
        self.clear_inputs()
        self.print_unordered_list_to_result_box(self.__rental_service.get_current_list())

    def most_rented_movies(self):
        self.clear_result_box()
        self.clear_inputs()
        try:
            most_rented_movies = self.__rental_service.generate_most_rented_movies()
            if len(most_rented_movies) == 0:
                raise DataException("No movies have been rented!")
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_ordered_list_to_result_box(most_rented_movies)

    def most_active_clients(self):
        self.clear_result_box()
        self.clear_inputs()
        try:
            most_active_clients = self.__rental_service.generate_most_active_clients()
            if len(most_active_clients) == 0:
                raise DataException("No movies have been rented!")
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_ordered_list_to_result_box(most_active_clients)

    def overdue_movies(self):
        self.clear_result_box()
        self.clear_inputs()
        try:
            overdue_movies = self.__rental_service.generate_late_rentals()
            if len(overdue_movies) == 0:
                raise DataException("There are no overdue movies!")
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_ordered_list_to_result_box(overdue_movies)

    def undo(self):
        self.clear_result_box()
        self.clear_inputs()
        try:
            self.__operation_manager.undo()
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_line_to_result_box("Undo successful!")

    def redo(self):
        self.clear_result_box()
        self.clear_inputs()
        try:
            self.__operation_manager.redo()
        except ShopException as se:
            self.print_line_to_result_box(str(se))
        else:
            self.print_line_to_result_box("Redo successful!")

    def print_help(self):
        self.clear_result_box()
        self.clear_inputs()
        self.print_line_to_result_box("The buttons on a line control the actions related to the entity on that line\n")
        self.print_line_to_result_box("In order to add something, all fields except the search are necessary\n")
        self.print_line_to_result_box("In order to delete something, the only needed field is the ID\n")
        self.print_line_to_result_box("In order to list all entities, no field is required\n")
        self.print_line_to_result_box("In order to update something, all fields except the search are necessary\n")
        self.print_line_to_result_box("In order to search for something, only one field (the corresponding one must "
                                      "be completed\n")
        self.print_line_to_result_box("In order to rent a movie, all fields except the return date are necessary\n")
        self.print_line_to_result_box("In order to return a movie, only the rental id and the return date are "
                                      "necessary\n")
        self.print_line_to_result_box("Every other button requires no input\n")
        self.print_line_to_result_box("Dates must be given in the following format: DD/MM/YYYY")

    def _run_menu(self):
        window = tkinter.Tk()
        window.title("Movie Rentals")
        frm_entities = tkinter.Frame(master=window)
        frm_entities.pack(anchor=tkinter.N)

        frm_client = tkinter.Frame(master=frm_entities)
        frm_client.pack(anchor=tkinter.W, side=tkinter.TOP, fill=tkinter.X)

        frm_client_information = tkinter.Frame(master=frm_client)
        frm_client_information.pack(anchor=tkinter.W, side=tkinter.LEFT)
        lbl_client = tkinter.Label(master=frm_client_information, text="Client")
        lbl_client.pack(side=tkinter.LEFT)
        self._lbl_with_ent_client_id = LabelEntry(frm_client_information, "ID", 5)
        self._lbl_with_ent_client_id.pack(side=tkinter.LEFT)
        self._lbl_with_ent_client_name = LabelEntry(frm_client_information, "Name", 20)
        self._lbl_with_ent_client_name.pack(side=tkinter.LEFT)
        self._lbl_with_ent_client_search = LabelEntry(frm_client_information, "Search by everything")
        self._lbl_with_ent_client_search.pack(side=tkinter.LEFT)

        frm_client_buttons = tkinter.Frame(master=frm_client)
        frm_client_buttons.pack(anchor=tkinter.W, side=tkinter.RIGHT)
        btn_client_add = tkinter.Button(master=frm_client_buttons, text="ADD", command=self.add_client)
        btn_client_add.pack(side=tkinter.LEFT)
        btn_client_delete = tkinter.Button(master=frm_client_buttons, text="DELETE", command=self.delete_client)
        btn_client_delete.pack(side=tkinter.LEFT)
        btn_client_list = tkinter.Button(master=frm_client_buttons, text="LIST", command=self.list_clients)
        btn_client_list.pack(side=tkinter.LEFT)
        btn_client_update = tkinter.Button(master=frm_client_buttons, text="UPDATE", command=self.update_client)
        btn_client_update.pack(side=tkinter.LEFT)
        btn_client_search = tkinter.Button(master=frm_client_buttons, text="SEARCH", command=self.search_client)
        btn_client_search.pack(side=tkinter.LEFT)

        frm_movie = tkinter.Frame(master=frm_entities)
        frm_movie.pack(anchor=tkinter.W, side=tkinter.TOP, fill=tkinter.X)

        frm_movie_information = tkinter.Frame(master=frm_movie)
        frm_movie_information.pack(anchor=tkinter.W, side=tkinter.LEFT)
        lbl_movie = tkinter.Label(master=frm_movie_information, text="Movie")
        lbl_movie.pack(side=tkinter.LEFT)
        self._lbl_with_ent_movie_id = LabelEntry(frm_movie_information, "ID", 5)
        self._lbl_with_ent_movie_id.pack(side=tkinter.LEFT)
        self._lbl_with_ent_movie_title = LabelEntry(frm_movie_information, "Title", 20)
        self._lbl_with_ent_movie_title.pack(side=tkinter.LEFT)
        self._lbl_with_ent_movie_description = LabelEntry(frm_movie_information, "Description")
        self._lbl_with_ent_movie_description.pack(side=tkinter.LEFT)
        self._lbl_with_ent_movie_genre = LabelEntry(frm_movie_information, "Genre")
        self._lbl_with_ent_movie_genre.pack(side=tkinter.LEFT)
        self._lbl_with_ent_movie_search = LabelEntry(frm_movie_information, "Search by everything")
        self._lbl_with_ent_movie_search.pack(side=tkinter.LEFT)

        frm_movie_buttons = tkinter.Frame(master=frm_movie)
        frm_movie_buttons.pack(anchor=tkinter.W, side=tkinter.RIGHT)
        btn_movie_add = tkinter.Button(master=frm_movie_buttons, text="ADD", command=self.add_movie)
        btn_movie_add.pack(side=tkinter.LEFT)
        btn_movie_delete = tkinter.Button(master=frm_movie_buttons, text="DELETE", command=self.delete_movie)
        btn_movie_delete.pack(side=tkinter.LEFT)
        btn_movie_list = tkinter.Button(master=frm_movie_buttons, text="LIST", command=self.list_movies)
        btn_movie_list.pack(side=tkinter.LEFT)
        btn_movie_update = tkinter.Button(master=frm_movie_buttons, text="UPDATE", command=self.update_movie)
        btn_movie_update.pack(side=tkinter.LEFT)
        btn_movie_search = tkinter.Button(master=frm_movie_buttons, text="SEARCH", command=self.search_movie)
        btn_movie_search.pack(side=tkinter.LEFT)

        frm_rental = tkinter.Frame(master=frm_entities)
        frm_rental.pack(anchor=tkinter.W, side=tkinter.TOP, fill=tkinter.X)

        frm_rental_information = tkinter.Frame(master=frm_rental)
        frm_rental_information.pack(anchor=tkinter.W, side=tkinter.LEFT)
        lbl_rental = tkinter.Label(master=frm_rental_information, text="Rental")
        lbl_rental.pack(side=tkinter.LEFT)
        self._lbl_with_ent_rental_id = LabelEntry(frm_rental_information, "ID", 5)
        self._lbl_with_ent_rental_id.pack(side=tkinter.LEFT)
        self._lbl_with_ent_rental_movie_id = LabelEntry(frm_rental_information, "Movie ID", 5)
        self._lbl_with_ent_rental_movie_id.pack(side=tkinter.LEFT)
        self._lbl_with_ent_rental_client_id = LabelEntry(frm_rental_information, "Client ID", 5)
        self._lbl_with_ent_rental_client_id.pack(side=tkinter.LEFT)
        self._lbl_with_ent_rental_date = LabelEntry(frm_rental_information, "Rental date", 12)
        self._lbl_with_ent_rental_date.pack(side=tkinter.LEFT)
        self._lbl_with_ent_rental_due_date = LabelEntry(frm_rental_information, "Due date", 12)
        self._lbl_with_ent_rental_due_date.pack(side=tkinter.LEFT)
        self._lbl_with_ent_rental_return_date = LabelEntry(frm_rental_information, "Return date", 12)
        self._lbl_with_ent_rental_return_date.pack(side=tkinter.LEFT)

        frm_rental_buttons = tkinter.Frame(master=frm_rental)
        frm_rental_buttons.pack(anchor=tkinter.W, side=tkinter.RIGHT)
        btn_rent = tkinter.Button(master=frm_rental_buttons, text="RENT", command=self.rent_movie)
        btn_rent.pack(side=tkinter.LEFT)
        btn_return = tkinter.Button(master=frm_rental_buttons, text="RETURN", command=self.return_movie)
        btn_return.pack(side=tkinter.LEFT)
        btn_list_rentals = tkinter.Button(master=frm_rental_buttons, text="LIST", command=self.list_rentals)
        btn_list_rentals.pack(side=tkinter.LEFT)

        frm_bottom_line = tkinter.Frame(master=frm_entities)
        frm_bottom_line.pack(anchor=tkinter.W, side=tkinter.TOP, fill=tkinter.X)
        lbl_statistics = tkinter.Label(master=frm_bottom_line, text="Statistics:")
        lbl_statistics.pack(side=tkinter.LEFT)
        btn_most_rented_movies = tkinter.Button(master=frm_bottom_line, text="MOST RENTED MOVIES",
                                                command=self.most_rented_movies)
        btn_most_rented_movies.pack(side=tkinter.LEFT)
        btn_most_active_clients = tkinter.Button(master=frm_bottom_line, text="MOST ACTIVE CLIENTS",
                                                 command=self.most_active_clients)
        btn_most_active_clients.pack(side=tkinter.LEFT)
        btn_overdue_movies = tkinter.Button(master=frm_bottom_line, text="OVERDUE MOVIES", command=self.overdue_movies)
        btn_overdue_movies.pack(side=tkinter.LEFT)
        btn_help = tkinter.Button(master=frm_bottom_line, text="HELP", command=self.print_help)
        btn_help.pack(side=tkinter.RIGHT)
        btn_redo = tkinter.Button(master=frm_bottom_line, text="REDO", command=self.redo)
        btn_redo.pack(side=tkinter.RIGHT)
        btn_undo = tkinter.Button(master=frm_bottom_line, text="UNDO", command=self.undo)
        btn_undo.pack(side=tkinter.RIGHT)

        self._result_box = tkinter.Text(master=window, state="disabled")
        self._result_box.pack()

        window.mainloop()
