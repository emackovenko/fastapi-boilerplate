from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: int = Field(None, description="ID пользователя")

    class Config:
        validate_assignment = True
