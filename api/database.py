from tinydb import TinyDB
from settings import SETTINGS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

tweet_db_engine = create_engine(SETTINGS['TWEET_DATABASE_URL'])
tweet_db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=tweet_db_engine))

user_db_engine = create_engine(SETTINGS['USER_DATABASE_URL'])
user_db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=user_db_engine))

#settings_db = TinyDB(SETTINGS['SETTINGS_DATABASE_URL'])
