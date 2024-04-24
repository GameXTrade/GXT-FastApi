import jwt

from fastapi import  HTTPException, Request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


from datetime import datetime, timedelta, timezone

from app.services.config import SECRET_KEY, ALGORITHM

# JWT time config
Jason_Web_Token_Exp = {
    # timdedelta lib attr. 
    "seconds": 0,
    "minutes": 0,
    "hours": 24
}

def check_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token signature")
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid token format")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Issue with token: " + str(e))
    return True, decoded
    
    
def check_request_token(req: Request):
   
    token = req.cookies.get("jwt")
    try:
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


def create_token(id:str, name:str, is_verified:bool):
    payload_data = { 
        "sub": id,
        "name": name,
        "is_verified": is_verified,
        "exp": datetime.now(timezone.utc) + timedelta(**Jason_Web_Token_Exp)
    }

    token = jwt.encode(
        payload = payload_data,
        key = SECRET_KEY,
        algorithm = ALGORITHM
    )
    return token