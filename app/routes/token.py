from fastapi import APIRouter, Depends, HTTPException, Request
import jwt
from jwt.exceptions import ExpiredSignatureError

from app.operations.users import get_user
from sqlalchemy.orm import Session
from app.database.db import get_db

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
def refresh_token(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    return user.id, user.name