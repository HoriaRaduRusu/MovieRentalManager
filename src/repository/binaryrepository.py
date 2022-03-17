import pickle

from repository.repo import Repository


class BinaryRepository(Repository):
    def __init__(self, validator_class, error_class, file_name):
        super().__init__(validator_class, error_class)
        self.__file_name = file_name
        self.__load()

    def add(self, entity):
        """
        Adds a given entity to the binary repository
        :param entity: The entity that will be added to the repo
        :return: nothing
        """
        super().add(entity)
        self.__save_to_file()

    def remove(self, entity_id):
        """
        Removes the entity with a given ID from the binary repository
        :param entity_id: The ID of the entity to be removed
        :return: The removed entity
        """
        removed_entity = super().remove(entity_id)
        self.__save_to_file()
        return removed_entity

    def update(self, entity):
        """
        Updates an entity from the binary repository
        :param entity: The updated form of the entity
        :return: The old form of the entity
        """
        old_entity = super().update(entity)
        self.__save_to_file()
        return old_entity

    def __load(self):
        """
        Loads the entities located in the associated binary file into the repository
        :return: nothing
        """
        with open(self.__file_name, "rb") as f:
            entities = pickle.load(f)
            for entity in entities:
                super().add(entities[entity])

    def __save_to_file(self):
        """
        Loads the entities located in the current repository to the associated binary file
        :return: nothing
        """
        with open(self.__file_name, "wb") as file:
            pickle.dump(self.entities, file)
