from app.schemas.user_schema import UserCreate
from app.models import model
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.operations.auth import generate_hash_password

# GET USER

def get_user(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()

def get_users(db:Session, skip: int = 0, limit: int = 100):    
    return db.query(model.User).offset(skip).limit(limit).all()


# CREATE USER
def create_new_user(db:Session, user: UserCreate): 
    hashpassword = generate_hash_password(user.password)
    db_user = model.User(username = user.username, email = user.email, image = user.image, hashedpassword = hashpassword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# DELETE USER
def delete_user(db:Session, user_id: int):
    db_user = db.query(model.User).filter(model.User.id==user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    else:
        return False
    
# VERIFY USER

class Message(BaseModel):
    code: str
    message: str

def verify_user_id(db:Session, user_id: int):
    db_user = db.query(model.User).filter(model.User.id==user_id).first()
    if db_user:
        if db_user.is_verified:
            return Message(code="NOT OK", message="Link is no longer valid. User already verified.")
        else:
            db_user.is_verified = 1
            db.commit()
            return Message(code="OK", message="User verified successfully")
    else:
        return Message(code="ERROR VERIFY USER ID", message="User not found")