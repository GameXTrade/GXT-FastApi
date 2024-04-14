from app.services.mailer import send_mail, MailBody
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.schemas.user_schema import UserCreate
from app.database.db import db_dependency
from app.operations.users import create_user, get_users,delete_user



router = APIRouter(
    prefix="/user", 
    tags=['user']
)


# GET ALL
@router.get("")
async def get_all_users(db: db_dependency, skip: int = 0, limit: int = 100):
    db_user = get_users(db, skip, limit)
    return db_user

# POST TEST
@router.post("", status_code=status.HTTP_201_CREATED)
async def add_one_user(db: db_dependency, user: UserCreate):
    db_user = create_user(db, user)
    return db_user
# PUT
@router.put("/{user_id}")
async def edite_one_user(user_id:str):

    return f"update user: {user_id}"

# DELETE ONE
@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_one_user(db: db_dependency, user_id: int):
    db_user = delete_user(db, user_id)
    if db_user:
        print(f"db_user mit der id: {user_id} erfolgreich gelöscht")
    else:
        print(f"kein user mit der id: {user_id} gefunden")
    return Response(status_code = status.HTTP_204_NO_CONTENT)

# POST
# @router.post("", response_model=User)
# def add_user(user_create: UserCreate, db: Session = Depends(get_db)):
#     '''Create new user in database'''
#     db_user = get_user_by_email(db, email = user_create.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail = "Email already registered")
#     db_user = create_user(db, user=user_create)

#     token = create_token(id = db_user.id, name=db_user.name)
#     send_mail({"to":[db_user.email],"subject":"Verify your email address 🚀","body":token})
#     return db_user
