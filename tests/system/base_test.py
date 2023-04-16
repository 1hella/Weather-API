from unittest import TestCase
from main import app


class BaseTest(TestCase):
    def setUp(self):
        self.app = app.test_client
