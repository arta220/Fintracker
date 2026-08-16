from dataclasses import field

from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator

from app.DTO.general import UpdateDTO


class GoalResponse(BaseModel):

    id:int = Field(...)
    name: str = Field(..., min_length=1, max_length=20)
    dueDate: str | None
    targetSum: float = Field(...)
    currentSum:float = Field(...)
    description: str = Field(max_length=200)
    colour: str = Field(min_length=6, max_length=6)
    model_config = ConfigDict(from_attributes=True)

class GoalDTO(BaseModel):
    id:int = Field(...)
    name: str = Field(..., min_length=1, max_length=20)
    dueDate: str | None
    targetSum: float = Field(...)
    currentSum:float = Field(...)
    description: str = Field(max_length=200)
    colour: str = Field(min_length=6, max_length=6)


class GoalCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    dueDate: str | None
    targetSum: float = Field(...)
    currentSum:float = Field(...)
    description: str = Field(max_length=200)
    colour: str = Field(min_length=6, max_length=6)


class GoalUpdateDTO(UpdateDTO):

    name: str | None = Field(..., min_length=1, max_length=20)
    dueDate: str | None
    targetSum: float | None = Field(...)
    currentSum:float  | None= Field(...)
    description: str  | None= Field(max_length=200)
    colour: str |None = Field(min_length=6, max_length=6)


