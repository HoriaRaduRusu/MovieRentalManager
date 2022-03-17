class Client:
    def __init__(self, client_id, name):
        """
        Creates a new client
        :param client_id: The client's ID
        :param name: The client's name
        """
        self.__client_id = client_id
        self.__name = name

    @property
    def id(self):
        return self.__client_id

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return "-" * 10 + " ID: " + str(self.id) + " " + "-" * 10 + "\nName: " + self.name
