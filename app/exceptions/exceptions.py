from sqlalchemy import exc


class AppError(Exception):
    pass

class InvalidToken(Exception):
    pass

class ExpiredToken(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class WrongPasswordError(Exception):
    pass

#описать чо писать в случае ошибок