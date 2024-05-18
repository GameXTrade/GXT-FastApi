from fastapi import APIRouter, Depends, Request
from app.operations.token import Token, check_request_token
from app.schemas.item_schema import ItemCreate
from app.operations.items import create_item, get_items_by_user_id, get_all_items, get_10_recently_added_items
from app.database.db import db_dependency

# only when payload is no used
# from app.operations.auth import authenticate_route


router = APIRouter(
    prefix="/item", 
    tags=['item']
)

@router.get("/all")
async def get_items(db: db_dependency, skip: int = 0, limit: int = 100):
    '''
    Endpoint: /item/all

    Retrieves all items from the database.
    
    Parameters:
    - db: Database connection provided by db_dependency.
    - skip: Number of records to skip. Default is 0.
    - limit: Maximum number of records to return. Default is 100.
    
    Returns:
    - List of all items from the database.
    '''
    db_items = await get_all_items(db, skip, limit)
    return db_items


@router.get("/recent")
async def ten_recently_added_items(db: db_dependency):
    return await get_10_recently_added_items(db)


@router.post("/create")
async def add_item_to_db(
    db: db_dependency, 
    item: ItemCreate, 
    token_data: Token = Depends(check_request_token)
):
    """
    Endpoint to add an item to the database associated with the authenticated user.

    Args:
    - item (ItemCreate): Item data including name, description, etc.
    - db (Session): Database session dependency.
    - token_data (Token): Token data dependency containing user information.

    Returns:
    - Item: The newly created item associated with the authenticated user.
    """

    token_payload = Token(**token_data) 
 
    db_item = create_item(db, item , user_id= token_payload.sub)
    return db_item





@router.get("")
async def get_user_items(
    db: db_dependency, 
    skip: int = 0, 
    limit: int = 100, 
    token_data: Token = Depends(check_request_token)
):
    """
    Endpoint to retrieve items associated with the authenticated user.

    Args:
    - db (Session): Database session dependency.
    - skip (int): Number of items to skip.
    - limit (int): Maximum number of items to retrieve.
    - token_data (Token): Token data dependency containing user information.

    Returns:
    - List[Item]: List of items associated with the authenticated user.
    """
    db_items = await get_items_by_user_id(db, user_id=token_data["sub"], skip=skip, limit=limit)
    return db_items