import json

from repository.repo import Repository


class JSONRepository(Repository):
    def __init__(self, validator_class, error_class, data_access_class, file_name):
        super().__init__(validator_class, error_class)
        self.__data_access_class = data_access_class
        self.__file_name = file_name
        self.__load()

    def add(self, entity):
        """
        Adds a given entity to the JSON repository
        :param entity: The entity that will be added to the repo
        :return: nothing
        """
        super().add(entity)
        self.__save_to_file()

    def update(self, entity):
        """
        Updates an entity from the JSON repository
        :param entity: The updated form of the entity
        :return: The old form of the entity
        """
        old_entity = super().update(entity)
        self.__save_to_file()
        return old_entity

    def remove(self, entity_id):
        """
        Removes the entity with a given ID from the JSON repository
        :param entity_id: The ID of the entity to be removed
        :return: The removed entity
        """
        removed_entity = super().remove(entity_id)
        self.__save_to_file()
        return removed_entity

    def __load(self):
        """
        Loads the entities located in the associated JSON file into the repository
        :return: nothing
        """
        with open(self.__file_name, "rt") as f:
            entities = json.load(f)
            for entity in entities.values():
                super().add(self.__data_access_class.deserializer(entity))

    def __save_to_file(self):
        """
        Loads the entities located in the current repository to the associated JSON file
        :return: nothing
        """
        with open(self.__file_name, "wt") as file:
            json.dump(self.entities, file, default=self.__data_access_class.serializer, indent=4)
