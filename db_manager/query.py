from sqlalchemy import text
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from db_manager.shem import UserShem
from db_manager.engine import asyncSession
from db_manager.models import User


async def add_user(user : UserShem.model_dump):
    async with asyncSession() as ssn:
        stmt = User(**user)
        ssn.add(stmt)
        await ssn.commit()
    

async def get_user(user : UserShem.model_dump):
    async with asyncSession() as ssn:
        query = select(User).filter_by(**user)
        result = await ssn.execute(query)
        return result.scalars().first()
    
async def get_password_to_email(email : str):
    async with asyncSession() as ssn:
        print(email)
        queru = text("SELECT password FROM user_table WHERE email=:email;")
        print(queru)
        result = await ssn.execute(queru, {"email": email})
        return result.one_or_none()
    