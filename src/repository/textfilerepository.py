from repository.repo import Repository


class TextFileRepository(Repository):
    def __init__(self, validator_class, error_class, data_access_class, file_name):
        super().__init__(validator_class, error_class)
        self.__data_access_class = data_access_class
        self.__file_name = file_name
        self.__load()

    def add(self, entity):
        """
        Adds a given entity to the text file repository
        :param entity: The entity that will be added to the repo
        :return: nothing
        """
        super().add(entity)
        with open(self.__file_name, "wt") as f:
            for entity in self.entities:
                self.__save_to_file(f, self.entities[entity])

    def remove(self, entity_id):
        """
        Removes the entity with a given ID from the text file repository
        :param entity_id: The ID of the entity to be removed
        :return: The removed entity
        """
        removed_entity = super().remove(entity_id)
        with open(self.__file_name, "wt") as f:
            for entity in self.entities:
                self.__save_to_file(f, self.entities[entity])
        return removed_entity

    def update(self, entity):
        """
        Updates an entity from the text file repository
        :param entity: The updated form of the entity
        :return: The old form of the entity
        """
        old_entity = super().update(entity)
        with open(self.__file_name, "wt") as f:
            for entity in self.entities:
                self.__save_to_file(f, self.entities[entity])
        return old_entity

    def __load(self):
        """
        Loads the entities located in the associated text file into the repository
        :return: nothing
        """
        with open(self.__file_name, "rt") as f:
            for line in f:
                new_entity = self.__data_access_class.read_from(line)
                super().add(new_entity)

    def __save_to_file(self, file, entity):
        """
        Loads an entity located in the current repository to the associated text file
        :param file: The File object describing the associated text file open for writing
        :param entity: The entity to be saved to the file
        :return: nothing
        """
        self.__data_access_class.write_to(file, entity)
