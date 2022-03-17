import traceback

from UI.MovieRentalGUI import MovieRentalGUI
from UI.MovieRentalUI import MovieRentalUI
from domain.settings import Settings
from domain.validators import ClientValidator, MovieValidator, RentalValidator, ClientException, MovieException, \
    RentalException, SettingsException
from repository.binaryrepository import BinaryRepository
from repository.jsondataaccessentity import ClientJSONDataAccess, MovieJSONDataAccess, RentalJSONDataAccess
from repository.jsonrepository import JSONRepository
from repository.repo import Repository
from repository.sqldataaccessentity import ClientSQLDataAccess, MovieSQLDataAccess, RentalSQLDataAccess
from repository.sqlrepository import SQLRepository
from repository.textdataaccessentity import ClientTextDataAccess, MovieTextDataAccess, RentalTextDataAccess
from repository.textfilerepository import TextFileRepository
from services.clientservice import ClientService
from services.movieservice import MovieService
from services.rentalservice import RentalService
from services.undoredo import OperationManager

if __name__ == "__main__":
    try:
        file_location = "../Data/"
        settings = Settings(file_location + "settings.properties")
        client_repo_lct = file_location + settings.client_repo
        movie_repo_lct = file_location + settings.movie_repo
        rental_repo_lct = file_location + settings.rental_repo
        if settings.repo_type == "inmemory":
            client_repo = Repository(ClientValidator, ClientException)
            movie_repo = Repository(MovieValidator, MovieException)
            rental_repo = Repository(RentalValidator, RentalException)
        elif settings.repo_type == "textfiles":
            client_repo = TextFileRepository(ClientValidator, ClientException, ClientTextDataAccess(), client_repo_lct)
            movie_repo = TextFileRepository(MovieValidator, MovieException, MovieTextDataAccess(), movie_repo_lct)
            rental_repo = TextFileRepository(RentalValidator, RentalException, RentalTextDataAccess(), rental_repo_lct)
        elif settings.repo_type == "binaryfiles":
            client_repo = BinaryRepository(ClientValidator, ClientException, client_repo_lct)
            movie_repo = BinaryRepository(MovieValidator, MovieException, movie_repo_lct)
            rental_repo = BinaryRepository(RentalValidator, RentalException, rental_repo_lct)
        elif settings.repo_type == "jsonfiles":
            client_repo = JSONRepository(ClientValidator, ClientException, ClientJSONDataAccess(), client_repo_lct)
            movie_repo = JSONRepository(MovieValidator, MovieException, MovieJSONDataAccess(), movie_repo_lct)
            rental_repo = JSONRepository(RentalValidator, RentalException, RentalJSONDataAccess(), rental_repo_lct)
        elif settings.repo_type == "sqlfiles":
            client_repo = SQLRepository(ClientValidator, ClientException, ClientSQLDataAccess(), client_repo_lct,
                                        "clients")
            movie_repo = SQLRepository(MovieValidator, MovieException, MovieSQLDataAccess(), movie_repo_lct, "movies")
            rental_repo = SQLRepository(RentalValidator, RentalException, RentalSQLDataAccess(), rental_repo_lct,
                                        "rentals")
        else:
            raise SettingsException("Invalid option!")
        client_service = ClientService(client_repo, rental_repo)
        movie_service = MovieService(movie_repo, rental_repo)
        rental_service = RentalService(client_repo, movie_repo, rental_repo)
        if settings.repo_type == "inmemory":
            client_service.generate_starting_clients()
            movie_service.generate_starting_movies()
            rental_service.generate_starting_rentals()
        operation_manager = OperationManager()
        if settings.ui_type == "Console":
            UI = MovieRentalUI(client_service, movie_service, rental_service, operation_manager)
            done = False
            while not done:
                try:
                    done = UI.run_menu()
                except Exception as ex:
                    print("Unexpected exception!", ex)
                    traceback.print_exc()
        elif settings.ui_type == "GUI":
            GUI = MovieRentalGUI(client_service, movie_service, rental_service, operation_manager)
    except OSError as ose:
        print("Invalid files!" + str(ose))
    except SettingsException as se:
        print("Invalid options!" + str(se))
