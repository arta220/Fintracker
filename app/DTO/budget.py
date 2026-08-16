from dataclasses import field
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator

from app.DTO.general import UpdateDTO


class BudgetResponse(BaseModel):

    id:int = Field(...)
    name: str = Field(..., min_length=1, max_length=20)
    limit: float = Field(...)
    colour: str = Field(min_length=6, max_length=6)
    model_config = ConfigDict(from_attributes=True)

class BudgetDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    limit: float = Field(...)
    colour: str = Field(min_length=6, max_length=6)


class BudgetCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    limit: float = Field(...)
    colour: str = Field(min_length=6, max_length=6)

class BudgetUpdateDTO(UpdateDTO):

    name: str = Field(min_length=1, max_length=20)
    limit: float
    colour: str = Field(min_length=6, max_length=6)


