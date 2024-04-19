from typing import Annotated
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends


from services.config import POSTGRESQL_ACCESS_URL



engine = create_engine(POSTGRESQL_ACCESS_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]