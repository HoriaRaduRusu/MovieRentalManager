from dataclasses import dataclass

from domain.validators import UndoRedoException


@dataclass
class FunctionCall:
    target_object: object
    handler: object
    args: tuple


@dataclass
class UndoRedoOperation:
    undo_operation: object
    redo_operation: object


class OperationManager:
    def __init__(self):
        self._operations = []
        self._index = -1

    def record_operation(self, operation):
        """
        Adds a new operation to the operations list and updates the list
        :param operation: The operation to be added
        :return: nothing
        """
        self._operations = self._operations[:self._index + 1]
        self._operations.append(operation)
        self._index += 1

    def undo(self):
        """
        Undoes the operation that is pointed by the index
        :return: nothing
        Raises an UndoRedoException if no undoes are possible (meaning index = -1)
        """
        if self._index == -1:
            raise UndoRedoException("No more undo operations are possible!")

        undo_operation = self._operations[self._index].undo_operation
        undo_operation.handler(undo_operation.target_object, *undo_operation.args)
        self._index -= 1

    def redo(self):
        """
        Redoes the last operation that was undone
        :return: nothing
        Raises an UndoRedoException if no redoes are possible (meaning index = len(operations)-1)
        """
        if self._index == len(self._operations) - 1:
            raise UndoRedoException("No more redo operations are possible!")

        self._index += 1
        redo_operation = self._operations[self._index].redo_operation
        redo_operation.handler(redo_operation.target_object, *redo_operation.args)
