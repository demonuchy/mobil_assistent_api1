from pydantic import BaseModel


class UserShem(BaseModel):
    email : str
    password : str
