import jwt
from fastapi import Request, HTTPException
from datetime import timedelta
from db_manager import query
from db_manager.config import settings


def create_access_token(data: dict, expires_delta: timedelta = None):
    payload = data.copy()
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def decode_jwt_token(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    
async def verefy_token(request : Request):
    authorization = request.headers.get("Authorization")
    print(authorization)
    if not authorization:
        raise HTTPException(status_code=402 , detail="Forbiden")
    token = authorization.split(" ")[1]
    print(token)
    payload : dict = decode_jwt_token(token, settings.SECRET_KEY)
    print(payload)
    email = payload.get("email")
    password = payload.get("password")
    password_db = await query.get_password_to_email(email)
    print(password_db)
    if not password_db or password != password_db[0]:
        raise HTTPException(status_code=403 , detail="Forbiden")


   