from app.services.mailer import send_mail
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.schemas.user_schema import UserCreate
from app.database.db import db_dependency
from app.operations.users import create_user, get_users,delete_user, get_user_by_email, verify_user_id, get_user
from app.operations.token import create_token, check_token, check_request_token
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

router = APIRouter(
    prefix="/user", 
    tags=['user']
)

class Token(BaseModel):
    sub: int
    name: str
    exp: int
    is_verified: bool
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

# GET ALL url/user
@router.get("")
async def get_all_users(db: db_dependency, skip: int = 0, limit: int = 100,  verify: bool = Depends(check_request_token)):
    db_users = get_users(db, skip, limit)
    return db_users


class UserEmail(BaseModel):
    email: str


# POST LOGIN url/user/login
@router.post("/login")
async def login_user(db:db_dependency, user: UserEmail):
    db_user = get_user_by_email(db, email = user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="email error")
    token = create_token(db_user.id, db_user.username, db_user.is_verified)
    send_mail({"to":[db_user.email],"subject":"Verify your email address 🚀","body":token},template="login")
    return {"token":"", "code": "Check your email inbox."}


class TokenRequest(BaseModel):
    token: str

# url/user/login-user
@router.post("/login-user")
async def login_user_token(token_request: TokenRequest, response: Response):
    # checkt den token ob er gültig ist
    token = token_request.token
    decoded_token = check_token(token)
  
    response.set_cookie(
        key="jwt",
        value=token,
        httponly=True,
        expires=datetime.now(timezone.utc) + timedelta(hours=24),  # Beispiel: Cookie läuft nach einem Tag ab
        #secure=True,  # Setze auf True, wenn die Verbindung über HTTPS erfolgt
        #samesite="strict",
    )
    return {"token":decoded_token, "code": "login succeed"}
    


# POST url/user
@router.post("", status_code=status.HTTP_201_CREATED)
async def add_user(db: db_dependency, user: UserCreate, response: Response):
    '''Create new user in database'''
    db_user = get_user_by_email(db, email = user.email)
    if db_user: # User email existiert bereits
        raise HTTPException(status_code=400, detail="not allowed to use this email")
    db_user = create_user(db, user)

    token = create_token(db_user.id, db_user.username, db_user.is_verified)
    
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
    return {"token":token, "code": "Verify your email in your email inbox."}


# PUT url/user/{user_id}
@router.put("/{user_id}")
async def edite_one_user(user_id:str, verify: bool = Depends(check_request_token)):

    return f"update user: {user_id}"


# DELETE ONE url/user/{user_id}
@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_one_user(db: db_dependency, user_id: int):
    db_user = delete_user(db, user_id)
    if db_user:
        print(f"db_user mit der id: {user_id} erfolgreich gelöscht")
    else:
        print(f"kein user mit der id: {user_id} gefunden")
    return Response(status_code = status.HTTP_204_NO_CONTENT)