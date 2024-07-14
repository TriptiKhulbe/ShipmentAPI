import logging

from sqlalchemy.orm import Session


class Service:
    def __init__(self, session: Session):
        self.session = session
        self.log = logging.getLogger(self.__class__.__name__)
