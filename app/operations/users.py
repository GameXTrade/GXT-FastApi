from app.schemas.user_schema import UserCreate
from app.models import model
from sqlalchemy.orm import Session

# User section

def get_user(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()

def get_users(db:Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()

def create_user(db:Session, user: UserCreate): 
    db_user = model.User(username = user.username, email = user.email, image = user.image)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session, user_id: int):
    db_user = db.query(model.User).filter(model.User.id==user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    else:
        return False