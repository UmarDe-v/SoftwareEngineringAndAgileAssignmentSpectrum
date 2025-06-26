from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:us191001@localhost:5432/spectrum"
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_lE0hw7zOeNTR@ep-shy-meadow-a9slytfp-pooler.gwc.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
#this is hardcoded for testinb ut change it if needed currently using neon

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# This file sets up the database connection using SQLAlchemy. It connects to a local PostgreSQL database 
# called "spectrum". A SessionLocal is created for handling individual DB sessions. The get_db function manages 
# the session lifecycle—opening it for use and closing it afterwards to prevent resource leaks.
