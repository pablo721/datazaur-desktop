

from sqlalchemy import MetaData, create_engine, select
from sqlalchemy.orm import Session

from .models import User, APIKeys, Base, ArbitrageAlgorithm
import yaml


class DBZaur:
    def __init__(self):
        self.filepath = 'db678.db'

        self.engine = create_engine(f'sqlite:///{self.filepath}', echo=True)

        self.meta = MetaData()