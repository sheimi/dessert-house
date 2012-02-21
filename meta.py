"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

__all__ = ['Session', 'engine', 'metadata']

# SQLAlchemy database engine. Updated by model.init_model()
#engine = create_engine("sqlite:///tutorial.db", echo=True)
engine = create_engine("sqlite:///tutorial.db", echo=False)

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database
metadata = MetaData()

# declarative table definitions
Base = declarative_base()

# session
Session = sessionmaker(bind=engine) 
session = Session()

def obj2dict(obj):
  d = {}
  for column in obj.__table__.columns.keys():
    d[column] = getattr(obj, column)
  return d
