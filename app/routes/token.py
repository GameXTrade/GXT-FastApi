from fastapi import APIRouter, Depends, HTTPException, Request
import jwt
from jwt.exceptions import ExpiredSignatureError

from app.operations.users import get_user
from app.operations.token import create_token
from app.services.mailer import send_mail
from sqlalchemy.orm import Session
from app.database.db import get_db

from app.operations.token import check_token, check_request_token


from app.database.db import db_dependency

router = APIRouter(
    prefix="/token", 
    tags=['token']
)


@router.get("")
def test_token(verify: bool = Depends(check_request_token)):
    return verify

@router.get("/refresh/{user_id}")
async def refresh_token(db: db_dependency, user_id: int):
    user = get_user(db, user_id)
    
    token = create_token(user.id, user.username)
    
    send_mail({"to":[user.email],"subject":"Verify your email address 🚀","body":token})
    return f"Neuen token an {user} erfolgreich gesendet"