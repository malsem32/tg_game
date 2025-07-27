from pymongo import MongoClient
from bot.pydantic_models import user_models

# Подключение к локальному серверу MongoDB
client = MongoClient('localhost', 27017)


class User_DB:
    def __init__(self):
        self.db_users = client['user_db']['users']
        self.db_invite_link = client['user_db']['invite_link']
        self.db_user_from_invite_link = client['user_db']['user_from_invite_link']

    def check_user(self, user: user_models.UserData):
        try:
            user_info = self.db_users.find_one({'user_id': user.user_id})
            if user_info is None:
                self.db_users.insert_one({'user_id': user.user_id,
                                          'username': user.username,
                                          'first_name': user.first_name,
                                          'last_name': user.last_name,
                                          'is_premium': user.is_premium,
                                          'photo_url': user.photo_url})
            else:
                self.db_users.update_one({'user_id': user
                                          .user_id}, {'$set':{
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_premium': user.is_premium,
                    'photo_url': user.photo_url
                }})
            return True
        except Exception as e:
            print(e)
            return False

    def check_invite_link(self, user_id: int, invite_link: str):
        data_info = self.db_invite_link.find_one({'user_id': user_id})
        if data_info is None:
            self.db_invite_link.insert_one({'user_id': user_id, 'invite_link': invite_link})
            return 1

    def check_user_for_invite_link(self, user_id: int):
        user_info = self.db_users.find_one({'user_id': user_id})
        if user_info is None:
            return None

    def user_from_invite_link(self, user_id: int, invite_link):
        self.db_user_from_invite_link.insert_one({'user_id': user_id, 'from_link': invite_link})

    def get_user_from_invite_link(self, invite_link: str):
        try:
            data_info = self.db_invite_link.find_one({'invite_link': invite_link})
            return data_info['user_id']
        except:
            return False
    def get_user_info_by_id(self, user_id: int):
        return self.db_users.find_one({'user_id': user_id})

