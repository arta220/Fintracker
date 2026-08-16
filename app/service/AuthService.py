
from app.repository.db_manager import DbManager
from app.repository.db_models import User
from app.repository.jwt import generate_token
from app.exceptions.exceptions import *
from app.DTO.user import*


#todo: подумать над специализированным менеджером
class AuthService:
    def __init__(self, db_manager:DbManager):
        self.dm_manager = db_manager
    def reg_user(self, data:UserRegisterDTO):
        user = self.dm_manager.create(User, data.model_dump())
        access_token = generate_token(user.id, "access")
        refresh_token = generate_token(user.id, "refresh")
        return UserAuthResponse(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token
        )


    def login_user(self, data:UserLoginDTO):
        selected_user = self.dm_manager.get_record(User, {"email" : data.email})

        if selected_user is None:
            raise UserNotFoundError
        if selected_user.password != data.password:
            raise WrongPasswordError

        access_token = generate_token(selected_user.id, "access")
        refresh_token = generate_token(selected_user.id, "refresh")

        return UserAuthResponse(
            user=selected_user,
            access_token=access_token,
            refresh_token=refresh_token
        )

    def update_user(self, data:UserUpdateDTO, user: User):
        return self.dm_manager.update(user, data)

    def delete_user(self, user: User):
        return self.dm_manager.delete(user)



