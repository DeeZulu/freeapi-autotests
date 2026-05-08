from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

class Avatar(BaseModel):
    _id: str
    local_path: str = Field(validation_alias="localPath")
    url: str


class User(BaseModel):
    __v: int
    _id: str
    avatar: Avatar
    created_at: str = Field(validation_alias="createdAt")
    email: str
    is_email_verified: bool = Field(validation_alias="isEmailVerified")
    login_type: str = Field(validation_alias="createdAt")
    role: str
    updated_at: str = Field(validation_alias="updatedAt")
    username: str


class Data(BaseModel):
    user: User


class UserRegisterResponse(BaseModel):
    data: Data
    message: str
    status_code: int = Field(validation_alias="statusCode")
    success: bool
