import configparser


class Settings:
    def __init__(self, file_name):
        self.__file_name = file_name
        self.__load()

    def __load(self):
        """
        Load the settings from the settings file into the program
        :return: nothing
        """
        config = configparser.ConfigParser()
        config.read(self.__file_name)
        self.__repo_type = config.get("DEFAULT", "repository").strip("\"")
        self.__client_repo = config.get("DEFAULT", "clients").strip("\"")
        self.__movie_repo = config.get("DEFAULT", "movies").strip("\"")
        self.__rental_repo = config.get("DEFAULT", "rentals").strip("\"")
        self.__ui_type = config.get("DEFAULT", "ui").strip("\"")

    @property
    def repo_type(self):
        return self.__repo_type

    @property
    def client_repo(self):
        return self.__client_repo

    @property
    def movie_repo(self):
        return self.__movie_repo

    @property
    def rental_repo(self):
        return self.__rental_repo

    @property
    def ui_type(self):
        return self.__ui_type
