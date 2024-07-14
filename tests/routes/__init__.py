from unittest import TestCase

from fastapi.testclient import TestClient

from src import create_app
from tests import initialize_memory_database


class TestRoutes(TestCase):
    def setUp(self):
        app = create_app()
        # override the Database.session set in the `create_app`
        # ideally, `routes` will never make db calls, all
        # database activities are done by the service.
        # to be on the safe side, to avoid anyone using
        # database session - will be eventually using an in-memory
        # empty database - without any tables.
        initialize_memory_database()
        # test client by fastapi - for mocking API calls.
        self.client = TestClient(app)