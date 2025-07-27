from pymongo import MongoClient
from bot.pydantic_models import user_models

# Подключение к локальному серверу MongoDB
client = MongoClient('localhost', 27017)


class Slaves_DB:
    def __init__(self):
        self.db_slaves = client['slaves_db']['user_slaves']

    def add_slave(self, user_id: int, slave_id: int):
        try:
            self.db_slaves.insert_one({'user_id': user_id, 'slave_id': slave_id})
            return True
        except:
            return False

    def get_slaves(self, user_id: int):
        try:
            data_info = self.db_slaves.find({'user_id': user_id})
            return data_info
        except:
            return False
