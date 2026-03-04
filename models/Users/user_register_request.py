from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    email: str
    password: str
    role: str
    username: str
