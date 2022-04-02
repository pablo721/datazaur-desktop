from sqlalchemy import MetaData, create_engine, select
from sqlalchemy.orm import Session

from .models import User, APIKeys, Base, ArbitrageAlgorithm
import yaml


class ChemicalDB:
    def __init__(self):
        self.filepath = 'db678.db'

        self.engine = create_engine(f'sqlite:///{self.filepath}', echo=True)

        self.meta = MetaData()
        self.config = None

        self.load_config()
        self.check_tables()

    def check_tables(self):
        with self.engine.begin() as connection:
            table_names = [row[0] for row in connection.execute("""SELECT name from sqlite_master WHERE type = 'table'; """).fetchall()]
            if 'users' not in table_names or 'keys' not in table_names:
                Base.metadata.create_all(self.engine)


    def load_config(self):
        try:
            with open('settings/settings.yaml', 'r') as config:
                self.config = yaml.safe_load(config)
        except:
            print('database cant find config file')

    def manage_session(self):
        pass

    def add_user(self, username, password_hash, salt, email):
        session = Session(self.engine)
        user = User(username=username, password_hash=password_hash, salt=salt, email=email)
        session.add(user)
        session.commit()

    def get_users(self):
        try:
            session = Session(self.engine)
            return [row[0] for row in session.query(User.username).all()]
        except:
            return None

    def get_hash_and_salt(self, username):
        try:
            session = Session(self.engine)
            hash_and_salt = session.execute(select(User.password_hash, User.salt).where(User.username == username)).all()
            return hash_and_salt[0]
        except:
            return None

    def show_users(self):
        try:
            session = Session(self.engine)
            print(session.execute("SELECT * from users").fetchall())
        except:
            return None

    def add_keys(self, user_id, exchange, public_key, private_key):
        try:
            session = Session(self.engine)
            session.add(APIKeys(user_id=user_id, exchange=exchange, public_key=public_key, private_key=private_key))
            session.commit()
        except:
            return None

    def get_keys(self, username):
        session = Session(self.engine)
        user_id = session.execute(select(User.user_id).where(User.username == username)).scalars().all()[0]
        if not user_id:
            return False
        keys = session.execute(select(APIKeys).where(APIKeys.user_id == user_id)).scalars().all()
        return keys



    def new_arbitrage_algorithm(self, **kwargs):
        try:
            session = Session(self.engine)
            algo = ArbitrageAlgorithm(**kwargs)
            session.add(algo)
            session.commit()
        except Exception as e:
            print(f'error: {e}')


    def config_arbitrage_algorithm(self, **kwargs):
        try:
            algo_id = kwargs['algorithm_id']
            session = Session(self.engine)
            algo = session.execute(select(ArbitrageAlgorithm).where(id=algo_id))
            for k, v in kwargs.items():
                algo[k] = v

            session.add(algo)
            session.commit()
        except Exception as e:
            print(f'error: {e}')


