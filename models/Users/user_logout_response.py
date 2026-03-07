from typing import Any, Dict

from pydantic import BaseModel, Field


class UserLogoutResponse(BaseModel):
    data: Dict[str, Any]
    message: str
    status_code: int = Field(validation_alias='statusCode')
    success: bool
