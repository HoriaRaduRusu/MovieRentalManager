class Movie:

    def __init__(self, movie_id, title, description, genre):
        """
        Creates a new movie
        :param movie_id: The movie's ID
        :param title: The movie's title
        :param description: The movie's description
        :param genre: The movie's genre
        """
        self.__movie_id = movie_id
        self.__title = title
        self.__description = description
        self.__genre = genre

    @property
    def id(self):
        return self.__movie_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def genre(self):
        return self.__genre

    def __str__(self):
        string = "-"*10 + " ID: " + str(self.id) + " " + "-" * 10 + "\n"
        string += "Title: " + self.title + "\nDescription: " + self.description + "\nGenre: " + self.genre
        return string
