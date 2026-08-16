
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator

from app.DTO.general import UpdateDTO


class TagResponse(BaseModel):
    id:int
    name: str = Field(...,min_length=1, max_length=20)
    model_config = ConfigDict(from_attributes=True)

class TagCreateDTO(BaseModel):
    name:str = Field(...,min_length=1, max_length=20)

class TagUpdateDTO(UpdateDTO):
    name:str = Field(...,min_length=1, max_length=20)