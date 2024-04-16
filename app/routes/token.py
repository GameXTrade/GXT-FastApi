from fastapi import APIRouter, Depends, HTTPException, Request
import jwt
from jwt.exceptions import ExpiredSignatureError

from app.operations.users import get_user
from app.operations.token import create_token
from app.services.mailer import send_mail
from sqlalchemy.orm import Session
from app.database.db import get_db

from app.database.db import db_dependency

router = APIRouter(
    prefix="/token", 
    tags=['token']
)

SECRET_KEY = 'WW3RXUHPWHUMI7737WMW6T43CUIP2P4I'
ALGORITHM = "HS256"

def check(req: Request):
    try:
        token = req.headers.get('Authorization', '').split(" ")[1]
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except KeyError:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid token format")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Issue with token: " + str(e))
    return True

@router.get("")
def test_token(verify: bool = Depends(check)):
    return verify

@router.get("/refresh/{user_id}")
async def refresh_token(db: db_dependency, user_id: int):
    user = get_user(db, user_id)
    
    token = create_token(user.id, user.username)
    
    send_mail({"to":[user.email],"subject":"Verify your email address 🚀","body":token})
    return f"Neuen token an {user} erfolgreich gesendet"