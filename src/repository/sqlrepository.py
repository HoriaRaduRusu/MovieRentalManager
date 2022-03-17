import sqlite3

from repository.repo import Repository


class SQLRepository(Repository):
    def __init__(self, validator_class, error_class, data_transfer_class, file_name, table_name):
        super().__init__(validator_class, error_class)
        self.__file_name = file_name
        self.__data_transfer_class = data_transfer_class
        self.__table_name = table_name
        self.__load()

    def add(self, entity):
        """
        Adds a given entity to the SQL repository
        :param entity: The entity that will be added to the repo
        :return: nothing
        """
        super().add(entity)
        self.__data_transfer_class.add(entity, self.__file_name)

    def remove(self, entity_id):
        """
        Removes the entity with a given ID from the SQL repository
        :param entity_id: The ID of the entity to be removed
        :return: The removed entity
        """
        removed_entity = super().remove(entity_id)
        self.__data_transfer_class.remove(entity_id, self.__file_name)
        return removed_entity

    def update(self, entity):
        """
        Updates an entity from the SQL repository
        :param entity: The updated form of the entity
        :return: The old form of the entity
        """
        updated_entity = super().update(entity)
        self.__data_transfer_class.update(entity, self.__file_name)
        return updated_entity

    def __load(self):
        """
        Loads the entities located in the associated SQL file into the repository
        :return: nothing
        """
        connection = sqlite3.connect(self.__file_name)
        cursor = connection.cursor()
        for elem in cursor.execute("SELECT * from " + self.__table_name):
            super().add(self.__data_transfer_class.read_from_line(elem))
        connection.close()
