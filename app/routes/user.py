from app.services.mailer import send_mail
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.schemas.user_schema import UserCreate
from app.database.db import db_dependency
from app.operations.users import create_user, get_users,delete_user, get_user_by_email, verify_user_id
from app.operations.token import create_token, check_token, Token, TokenRequest
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from app.operations.auth import authenticate_route, verify_password


router = APIRouter(
    prefix="/user", 
    tags=['user']
)

# not finished
@router.get("/verify-user")
async def verify_user(db: db_dependency, request: Request):
    '''
    Requires a valid HTTP-only JWT cookie (no token in URL query).
    Takes JWT, then decodes and verifies user via user ID.
    
    Parameters:
    - db: Database connection provided by db_dependency.
    - request: Request object used to access the JWT cookie.

    Returns:
    - If a valid JWT is found and the user is successfully verified:
        {'token': decoded_token, 'code': message.code}
    - Otherwise (if a valid JWT is not found):
        False
    '''

    token = request.cookies.get("jwt")
    is_decoded, decoded_token = check_token(token)
    if is_decoded:
        token_model = Token(**decoded_token)
        user_id = token_model.sub
        message = verify_user_id(db, user_id)
        return {"token":decoded_token, "code": message.code}
    
    return False

# GET ALL url/user
@router.get("")
@authenticate_route
async def get_first_100_users(db: db_dependency, skip: int = 0, limit: int = 100):
    '''
    Request to database requires valid JWT.
    Returns users.
    
    Parameters:
    - db: Database connection provided by db_dependency.
    - skip: Number of records to skip. Default is 0.
    - limit: Maximum number of records to return. Default is 100.
    # - verify: Boolean value provided by check_request_token dependency indicating whether JWT is verified.

    Returns:
    - List of user records from the database.
    '''
    db_users = get_users(db, skip, limit)
    return db_users


class UserCredentials(BaseModel):
    email: str
    password: str


# POST LOGIN url/user/login
@router.post("/login") 
async def login_user(db:db_dependency, user: UserCredentials, response: Response):
    '''
    Logs in a user and returns a JWT token for authentication.
    
    Parameters:
    - db: Database connection provided by db_dependency.
    - user: User credentials including email and password.
    - response: Response object to set the JWT token as a cookie.
    
    Returns:
    - Dictionary containing the JWT token and a success message if login is successful.
    
    Raises:
    - HTTPException(400): If the email does not exist in the database or if the password is incorrect.
    '''
    db_user = get_user_by_email(db, email = user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="email error")
    else:
        if verify_password(user.password, db_user.hashedpassword):
            token = create_token(db_user.id, db_user.username, db_user.is_verified, db_user.image)
    
            # response = JSONResponse({"message": "User created successfully"})
            response.set_cookie(
                key="jwt",
                value=token,
                httponly=True,
                expires=datetime.now(timezone.utc) + timedelta(hours=24),  # Beispiel: Cookie läuft nach einem Tag ab
                #secure=True,  # Setze auf True, wenn die Verbindung über HTTPS erfolgt
                #samesite="strict",
            )
            _, decoded_token = check_token(token)
        else:
            raise HTTPException(status_code=400, detail="login failed")
    return {"token": decoded_token, "code": "login succeed."}


# POST url/user
@router.post("", status_code=status.HTTP_201_CREATED)
async def add_user(db: db_dependency, user: UserCreate, response: Response):
    '''
    Creates a new user in the database.
    
    Parameters:
    - db: Database connection provided by db_dependency.
    - user: An object containing the user data to be created.
    - response: Response object used to set the HTTP-only cookie with the JWT and control the response.

    Returns:
    - If the user is successfully created:
        {'token': token, 'code': 'Verify your email in your email inbox.'}
    - Otherwise (if the email address already exists):
        An HTTP error with status code 400 and detail message "not allowed to use this email".
    '''
    db_user = get_user_by_email(db, email = user.email)
    if db_user: # User email existiert bereits
        raise HTTPException(status_code=400, detail="not allowed to use this email")
    db_user = create_user(db, user)

    token = create_token(db_user.id, db_user.username, db_user.is_verified, db_user.image)
    _, decoded_token = check_token(token)
    
    response.set_cookie(
        key="jwt", 
        value=token,
        httponly=True,
        expires=datetime.now(timezone.utc) + timedelta(hours=24),  # Beispiel: Cookie läuft nach einem Tag ab
        #secure=True,  # Setze auf True, wenn die Verbindung über HTTPS erfolgt
        #samesite="strict",

    )
    
    # send_mail({"to":[db_user.email],"subject":"Verify your email address 🚀"})
    return {"token": decoded_token, "code": "register succeed."}


# PUT url/user/{user_id}
@router.put("/{user_id}")
@authenticate_route
async def edite_one_user(user_id:str):
    '''
    Updates a user's data based on their ID.
    
    Parameters:
    - user_id: The ID of the user to be edited.
    - verify: Boolean value provided by the check_request_token dependency indicating whether JWT is verified.

    Returns:
    - A confirmation message that the user with the specified ID has been updated.
    '''
    return f"update user: {user_id}"


# DELETE ONE url/user/{user_id}
@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
@authenticate_route
async def delete_one_user(db: db_dependency, user_id: int):
    '''
    Deletes a user from the database based on their ID.
    
    Parameters:
    - db: Database connection provided by db_dependency.
    - user_id: The ID of the user to be deleted.
    - verify: Boolean value provided by the check_request_token dependency indicating whether JWT is verified.

    Returns:
    - An empty HTTP response with status code 204 (NO CONTENT).
    '''
    db_user = delete_user(db, user_id)
    if db_user:
        print(f"db_user mit der id: {user_id} erfolgreich gelöscht")
    else:
        print(f"kein user mit der id: {user_id} gefunden")
    return Response(status_code = status.HTTP_204_NO_CONTENT)