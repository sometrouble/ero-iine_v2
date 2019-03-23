import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

from database import tweet_db_engine

Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'eroiine'
    tweet_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)

    # for filtering dataset
    tweet_text = Column(String(300))
    image_url_1 = Column(String(50))
    image_url_2 = Column(String(50))
    image_url_3 = Column(String(50))
    image_url_4 = Column(String(50))

    tags = Column(Text())
    is_eroiine = Column(Boolean)

    def __init__(self, tweet_id: int, user_id: int, tweet_text: str, image_urls: list):
        self.tweet_id = tweet_id
        self.user_id = user_id
        self.tweet_text = tweet_text
        self.image_url_1 = image_urls[0]
        self.image_url_2 = image_urls[1]
        self.image_url_3 = image_urls[2]
        self.image_url_4 = image_urls[3]


if __name__ == '__main__':
    Base.metadata.create_all(tweet_db_engine)
