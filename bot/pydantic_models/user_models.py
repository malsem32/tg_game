from pydantic import BaseModel

class UserData(BaseModel):
    user_id: int
    username: str
    first_name: str
    last_name: str
    is_premium: bool
    photo_url: str
