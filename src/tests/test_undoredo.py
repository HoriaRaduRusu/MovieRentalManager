from unittest import TestCase

from domain.client import Client
from domain.validators import ClientValidator, ClientException, RentalValidator, RentalException, UndoRedoException
from repository.repo import Repository
from services.clientservice import ClientService
from services.handlers import UndoHandlers, RedoHandlers
from services.undoredo import OperationManager, UndoRedoOperation, FunctionCall


class TestOperationManager(TestCase):
    def setUp(self):
        self.client_repo = Repository(ClientValidator, ClientException)
        self.rental_repo = Repository(RentalValidator, RentalException)
        self.client_service = ClientService(self.client_repo, self.rental_repo)
        self.operation_manager = OperationManager()
        self.test_client1 = Client(1, "name1")
        self.client_repo.add(self.test_client1)
        undo_operation1 = FunctionCall(self.client_service, UndoHandlers.ADD_CLIENT, (1,))
        redo_operation1 = FunctionCall(self.client_service, RedoHandlers.ADD_CLIENT, (1, "name1"))
        self.operation_manager.record_operation(UndoRedoOperation(undo_operation1, redo_operation1))
        self.test_client2 = Client(2, "name2")
        self.client_repo.add(self.test_client2)
        undo_operation2 = FunctionCall(self.client_service, UndoHandlers.ADD_CLIENT, (2,))
        redo_operation2 = FunctionCall(self.client_service, RedoHandlers.ADD_CLIENT, (2, "name2"))
        self.operation_manager.record_operation(UndoRedoOperation(undo_operation2, redo_operation2))

    def test_record_operation(self):
        undo_operation = FunctionCall(self.client_service, UndoHandlers.ADD_CLIENT, (1,))
        redo_operation = FunctionCall(self.client_service, RedoHandlers.ADD_CLIENT, (1, "name"))
        self.operation_manager.record_operation(UndoRedoOperation(undo_operation, redo_operation))
        self.assertEqual(3, len(self.operation_manager._operations))
        self.assertEqual(2, self.operation_manager._index)

    def test_undo(self):
        self.operation_manager.undo()
        self.assertEqual(0, self.operation_manager._index)
        self.assertEqual(1, len(self.client_repo.entities))
        self.operation_manager.undo()
        self.assertRaises(UndoRedoException, self.operation_manager.undo)

    def test_redo(self):
        self.assertRaises(UndoRedoException, self.operation_manager.redo)
        self.operation_manager.undo()
        self.assertEqual(0, self.operation_manager._index)
        self.assertEqual(1, len(self.client_repo.entities))
        self.operation_manager.redo()
        self.assertEqual(1, self.operation_manager._index)
        self.assertEqual(2, len(self.client_repo.entities))
