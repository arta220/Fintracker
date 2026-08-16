from pydantic import BaseModel, Field, model_validator
from app.DTO.general import UpdateDTO
from app.DTO.tags import TagResponse

class TransactionResponse(BaseModel):

    id:int = Field(...)
    name: str = Field(...,min_length=1, max_length=20)
    sum:float = Field(...)
    description: str = Field(...,min_length=1, max_length=200)
    categoryId:int
    Tags: list[TagResponse]

class TransactionDTO(BaseModel):

    name: str = Field(...,min_length=1, max_length=20)
    sum:float = Field(...)
    description: str | None = Field(...,min_length=1, max_length=200)
    categoryId:int| None
    Tags: list[int] | None

class TransactionCreateDTO(BaseModel):

    name: str = Field(...,min_length=1, max_length=20)
    sum:float = Field(...)
    description:str|None= Field(...,min_length=1, max_length=200)
    categoryId:int| None
    tagIds:list[int]| None





class TransactionUpdateDTO(UpdateDTO):

    name: str | None = Field(default=None,min_length=1, max_length=20)
    sum:float | None=None
    description: str | None = Field(default=None,min_length=1, max_length=200)
    categoryId: int | None=None
    tagIds: list[int] | None=None


