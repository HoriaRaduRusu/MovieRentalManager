from src.repository.iterabledatastructure import IterableStructure


class Repository:
    def __init__(self, validator_class, error_class):
        """
        Creates a new repository
        :param validator_class: The class that is used to validate the repository objects
        :param error_class: The error class that should be raised if the repository operations are invalid
        """
        self.__entities = IterableStructure()
        self.__validator_class = validator_class
        self.__error_class = error_class

    @property
    def entities(self):
        return self.__entities

    def add(self, entity):
        """
        Validates and adds a new entity to the repository
        :param entity: The entity to be added
        :return: nothing
        Raise an error of type __error_class if an entity with the same ID as the given entity already exists
        """
        self.__validator_class.validate(entity)
        if entity.id in self.get_current_ids():
            raise self.__error_class("The ID already exists!")
        self.entities.append(entity)
        IterableStructure.sort(self.entities, lambda x, y: x.id < y.id)

    def remove(self, entity_id):
        """
        Removes the entity with a given ID from the repository
        :param entity_id: The ID of the entity
        :return: The removed entity
        """
        current_entity = self.get_entity_at_id(entity_id)
        if current_entity is not None:
            del self.entities[self.get_current_ids().index(entity_id)]
            return current_entity

    def update(self, entity):
        """
        Validates and updates a entity from the repository
        :param entity: The updated form of the entity
        :return: The old form of the entity
        """
        self.__validator_class.validate(entity)
        old_entity = self.get_entity_at_id(entity.id)
        if old_entity is not None:
            self.entities[self.get_current_ids().index(entity.id)] = entity
            return old_entity

    def get_current_ids(self):
        """
        Returns the list of current IDs from the repository
        :return: The list of current IDs from the repository
        """
        return [x.id for x in self.entities]

    def get_entity_at_id(self, entity_id):
        """
        Returns the entity with a specific ID
        :param entity_id: The ID of the entity
        :return: The entity at the specified ID
        Raise an error of type __error_class if an entity with the specified ID does not exist
        """
        current_ids = self.get_current_ids()
        if entity_id not in current_ids:
            raise self.__error_class("The ID doesn't exist!")
        return self.entities[current_ids.index(entity_id)]
