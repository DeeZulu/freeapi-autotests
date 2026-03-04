from pydantic import BaseModel, Field


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
    access_token: str = Field(validation_alias="accessToken")
    refresh_token: str = Field(validation_alias="refreshToken")
    user: User


class UserLoginResponse(BaseModel):
    data: Data
    message: str
    status_code: int = Field(validation_alias="statusCode")
    success: bool
