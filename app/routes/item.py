from fastapi import APIRouter, Depends
from app.operations.token import Token, check_request_token
from app.schemas.item_schema import ItemCreate
from app.operations.auth import authenticate_route
from app.operations.items import create_item, get_items_by_user_id, get_all_items
from app.database.db import db_dependency



router = APIRouter(
    prefix="/item", 
    tags=['item']
)

@router.post("/all")
async def get_items(db: db_dependency, skip: int = 0, limit: int = 100):
    db_items = get_all_items(db, skip, limit)
    return db_items

@router.post("/create")
async def test_item(db: db_dependency, item: ItemCreate, token_data: Token = Depends(check_request_token)):
    token_payload = Token(**token_data) 
    # print(token_payload)
    db_item = create_item(db, item , user_id= token_payload.sub)
    print(db_item, "create")
    return db_item

@router.get("")
async def test_items(db: db_dependency, skip: int = 0, limit: int = 100, token_data: Token = Depends(check_request_token)):
    db_items = get_items_by_user_id(db, user_id=token_data["sub"], skip=skip, limit=limit)
    return db_items