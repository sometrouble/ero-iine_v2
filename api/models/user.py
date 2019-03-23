import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import Column, Text
from sqlalchemy.ext.declarative import declarative_base

from database import user_db_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    hashed_user_id = Column(Text(), primary_key=True)
    token = Column(Text())
    token_secret = Column(Text())

    def __init__(self, hashed_user_id: int, token: str, token_secret: str):
        self.hashed_user_id = hashed_user_id
        self.token = token
        self.token_secret = token_secret


if __name__ == '__main__':
    Base.metadata.create_all(user_db_engine)
