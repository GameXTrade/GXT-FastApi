from app.services.mailer import send_mail, MailBody
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.schemas.user_schema import User, UserCreate
from app.database.db import db_dependency
from app.operations.users import create_user, get_users,delete_user, get_user_by_email, verify_user_id
from app.operations.token import create_token, check_token
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

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
async def add_user(db: db_dependency, user: UserCreate, response: Response):
    '''Create new user in database'''
    db_user = get_user_by_email(db, email = user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = create_user(db, user)

    token = create_token(db_user.id, db_user.username)
    
    # response = JSONResponse({"message": "User created successfully"})
    response.set_cookie(
        key="jwt",
        value=token,
        httponly=True,
        expires=datetime.now(timezone.utc) + timedelta(hours=24),  # Beispiel: Cookie läuft nach einem Tag ab
        #secure=True,  # Setze auf True, wenn die Verbindung über HTTPS erfolgt
        #samesite="strict",

    )
    
    send_mail({"to":[db_user.email],"subject":"Verify your email address 🚀"})
    return True

@router.get("/test-cookie")
async def test(response: Response):
    response.set_cookie(
        key="jwt",
        value="Test-cookie",
        httponly=True,
        expires=datetime.now(timezone.utc) + timedelta(hours=24),  # Beispiel: Cookie läuft nach einem Tag ab
        #secure=True,  # Setze auf True, wenn die Verbindung über HTTPS erfolgt
        #samesite="strict",
    )
    return True 


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

class Token(BaseModel):
    sub: int
    name: str
    exp: int
    class Config:
        from_attributes = True

@router.get("/verify-user")
async def verify_user(db: db_dependency, request: Request):
    token = request.cookies.get("jwt")
    decoded_token = check_token(token)
    if decoded_token:
        token_model = Token(**decoded_token)
        user_id = token_model.sub
        message = verify_user_id(db, user_id)
        return {"token":decoded_token, "code": message.code}
    
    return False