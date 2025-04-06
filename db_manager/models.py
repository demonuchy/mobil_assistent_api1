from sqlalchemy import ForeignKey, text, Column, BigInteger, String, Boolean, SmallInteger, DateTime
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class Base(DeclarativeBase): 
    pass

class User(Base):
    __tablename__ = "user_table"
    id = Column(BigInteger, primary_key=True)
    email = Column(String)
    password = Column(String)
