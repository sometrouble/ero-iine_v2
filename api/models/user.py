import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import Column, Text
from sqlalchemy.ext.declarative import declarative_base

from database import user_db_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    hashed_user_id = Column(Text(), primary_key=True)
    user_token = Column(Text())
    user_token_secret = Column(Text())

    def __init__(self, hashed_user_id: int, user_token: str, user_token_secret: str):
        self.hashed_user_id = hashed_user_id
        self.user_token = user_token
        self.user_token_secret = user_token_secret


if __name__ == '__main__':
    Base.metadata.create_all(user_db_engine)
