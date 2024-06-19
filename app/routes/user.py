from app.services.mailer import send_mail
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.schemas.user_schema import UserCreate
from app.database.db import db_dependency
from app.operations.users import create_new_user, get_users,delete_user, get_user_by_email, verify_user_id
from app.operations.token import create_token, check_token, Token, TokenRequest
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from app.operations.auth import authenticate_route, verify_password


router = APIRouter(
    prefix="/user", 
    tags=['user']
)

# not finished
# @router.get("/verify-user")
# async def verify_user(db: db_dependency, request: Request):

#     token = request.cookies.get("jwt")
#     is_decoded, decoded_token = check_token(token)
#     if is_decoded:
#         token_model = Token(**decoded_token)
#         user_id = token_model.sub
#         message = verify_user_id(db, user_id)
#         return {"token":decoded_token, "code": message.code}
    
#     return False


@router.get("")
@authenticate_route
async def get_first_100_users(db: db_dependency, skip: int = 0, limit: int = 100):
    """
    Retrieve the first 100 users.

    This endpoint fetches a list of users from the database with optional pagination. 
    The endpoint is protected and requires authentication.

    Parameters:
    - db (db_dependency): The database session.
    - skip (int, optional): The number of users to skip before starting to collect the result set. Default is 0.
    - limit (int, optional): The maximum number of users to return. Default is 100.

    Request Example:
    GET /user?skip=0&limit=100

    Responses:
    - 200 OK: Returns a list of users.
    - 401 Unauthorized: If the user is not authenticated.

    Example:
    GET /user?skip=0&limit=100
    """
    db_users = get_users(db, skip, limit)
    return db_users


class UserCredentials(BaseModel):
    email: str
    password: str


@router.post("/login") 
async def login_user(db:db_dependency, user: UserCredentials, response: Response):
    """
    Authenticate a user and issue a JWT token.

    This endpoint allows a user to log in by providing their email and password. If the credentials are correct, 
    a JWT token is issued and set as an HTTP-only cookie.

    Parameters:
    - db (db_dependency): The database session.
    - user (UserCredentials, required): The user credentials containing email and password.
    - response (Response): The response object to set cookies.

    Request Body Example:
    {
        "email": "user@example.com",
        "password": "userpassword"
    }

    Responses:
    - 200 OK: Returns the JWT token and a success message if login is successful.
    - 400 Bad Request: If the email is not found or the password is incorrect.

    Example:
    POST /user/login
    {
        "email": "user@example.com",
        "password": "userpassword"
    }
    """
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
                secure=True,  # Setze auf True, wenn die Verbindung über HTTPS erfolgt
                samesite="None",
            )
            _, decoded_token = check_token(token)

        else:
            raise HTTPException(status_code=400, detail="login failed")
    return {"token": decoded_token, "code": "login succeed."}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: UserCreate, response: Response):
    """
    Register a new user.

    This endpoint allows a new user to register by providing their email and other necessary details. 
    If the registration is successful, a JWT token is issued and set as an HTTP-only cookie.

    Parameters:
    - db (db_dependency): The database session.
    - user (UserCreate, required): The user data for registration.
    - response (Response): The response object to set cookies.

    Request Body Example:
    {
        "email": "newuser@example.com",
        "password": "newuserpassword",
        "username": "newuser"
    }

    Responses:
    - 201 Created: Returns the JWT token and a success message if registration is successful.
    - 400 Bad Request: If the email is already in use.

    Example:
    POST /user
    {
        "email": "newuser@example.com",
        "password": "newuserpassword",
        "username": "newuser"
    }
    """
    db_user = get_user_by_email(db, email = user.email)
    if db_user: # User email existiert bereits
        raise HTTPException(status_code=400, detail="not allowed to use this email")
    db_user = create_new_user(db, user)

    token = create_token(db_user.id, db_user.username, db_user.is_verified, db_user.image)
    _, decoded_token = check_token(token)
    
    response.set_cookie(
        key="jwt", 
        value=token,
        httponly=True,
        expires=datetime.now(timezone.utc) + timedelta(hours=24),  # Beispiel: Cookie läuft nach einem Tag ab
        secure=True,  # Setze auf True, wenn die Verbindung über HTTPS erfolgt
        samesite="None",

    )
    
    # send_mail({"to":[db_user.email],"subject":"Verify your email address 🚀"})
    return {"token": decoded_token, "code": "register succeed."}


# PUT url/user/{user_id}
# @router.put("/{user_id}")
# @authenticate_route
# async def edite_one_user(user_id:str):
#     '''
#     Updates a user's data based on their ID.
    
#     Parameters:
#     - user_id: The ID of the user to be edited.
#     - verify: Boolean value provided by the check_request_token dependency indicating whether JWT is verified.

#     Returns:
#     - A confirmation message that the user with the specified ID has been updated.
#     '''
#     return f"update user: {user_id}"


# DELETE ONE url/user/{user_id}
# @router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
# @authenticate_route
# async def delete_one_user(db: db_dependency, user_id: int):
#     '''
#     Deletes a user from the database based on their ID.
    
#     Parameters:
#     - db: Database connection provided by db_dependency.
#     - user_id: The ID of the user to be deleted.
#     - verify: Boolean value provided by the check_request_token dependency indicating whether JWT is verified.

#     Returns:
#     - An empty HTTP response with status code 204 (NO CONTENT).
#     '''
#     db_user = delete_user(db, user_id)
#     if db_user:
#         print(f"db_user mit der id: {user_id} erfolgreich gelöscht")
#     else:
#         print(f"kein user mit der id: {user_id} gefunden")
#     return Response(status_code = status.HTTP_204_NO_CONTENT)