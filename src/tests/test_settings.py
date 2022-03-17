from unittest import TestCase

from domain.settings import Settings


class TestSettings(TestCase):
    def setUp(self):
        self.settings = Settings("../../TestFiles/test_settings.properties")

    def test_repo_type(self):
        self.assertEqual(self.settings.repo_type, "textfiles")

    def test_client_repo(self):
        self.assertEqual(self.settings.client_repo, "repository1.txt")

    def test_movie_repo(self):
        self.assertEqual(self.settings.movie_repo, "repository2.txt")

    def test_rental_repo(self):
        self.assertEqual(self.settings.rental_repo, "repository3.txt")

    def test_ui_type(self):
        self.assertEqual(self.settings.ui_type, "GUI")
