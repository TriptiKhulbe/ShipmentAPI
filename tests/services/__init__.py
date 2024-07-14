from unittest import TestCase

from sqlalchemy import inspect, text

from src.commons.database import Database
from src.commons.models import Model
from tests import initialize_memory_database


class TestServices(TestCase):
    @classmethod
    def setUpClass(cls):
        initialize_memory_database()
        Model.metadata.create_all(Database.engine)
        Database.session.commit()

    def setUp(self):
        self.session = Database.session

    def tearDown(self) -> None:
        with Database.engine.connect() as connection:
            inspector = inspect(connection)
            table_names = inspector.get_table_names()

            for each_table in table_names:
                self.session.execute(text(f"DELETE FROM {each_table}"))
            self.session.commit()
