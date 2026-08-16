from app.repository import jwt
def refresh_access_token(user_id:int):
    return jwt.generate_token(user_id, "access" )


