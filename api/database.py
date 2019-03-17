from settings import SETTINGS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

db_engine = create_engine(SETTINGS['DATABASE_URL'])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))
