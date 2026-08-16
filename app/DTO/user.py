from dataclasses import field

from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator
class UserResponse(BaseModel):
    id: int
    name: str = Field(...,min_length=1, max_length=50)
    email:EmailStr = Field(..., max_length=50)
    created_at:str
    model_config=ConfigDict(from_attributes=True)

class UserRegisterDTO(BaseModel):
    name: str = Field(...,min_length=1, max_length=50)
    email: EmailStr = Field(..., max_length=50)
    password: str = Field(...,min_length=8,max_length=200)

class UserLoginDTO(BaseModel):
    email:EmailStr = Field(...,max_length=50)
    password: str = Field(...,min_length=8,max_length=200)

class UserUpdateDTO(BaseModel):
    name: str | None = Field(default=None,min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None,max_length=50)
    # password: str = Field(default=None,min_length=8,max_length=200)
    @model_validator(mode="after")
    def at_least_one_field(self):
        if self.name is None and self.email is None:
            raise ValueError("At least one field must be provided")
        return self

class PasswordUpdateDTO(BaseModel):
    old_password: str = Field(...,min_length=8,max_length=200)
    new_password: str = Field(...,min_length=8,max_length=200)

class UserAuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str