from pydantic import BaseModel, model_validator


class UpdateDTO(BaseModel):
    @model_validator(mode="after")
    def at_least_one_field(self):
        if not self.model_dump(exclude_unset=True):
            raise ValueError("At least one field must be provided")
        print(self.model_dump(exclude_unset=True))
        return self