from pydantic import BaseModel, Field


class Data(BaseModel):
    is_email_verified: bool = Field(validation_alias='isEmailVerified')


class VerifyEmailResponse(BaseModel):
    data: Data
    message: str
    status_code: int = Field(validation_alias='statusCode')
    success: bool