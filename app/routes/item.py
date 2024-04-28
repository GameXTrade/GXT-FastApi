from fastapi import APIRouter, Depends
from app.operations.token import Token, check_request_token
from app.schemas.item_schema import ItemCreate
from app.operations.auth import authenticate_route
from app.operations.items import create_item, get_items_by_user_id
from app.database.db import db_dependency



router = APIRouter(
    prefix="/item", 
    tags=['item']
)

@router.post("/create")
async def test_item(db: db_dependency, item: ItemCreate, token_data: Token = Depends(check_request_token)):
    token_payload = Token(**token_data) 
    # print(token_payload)
    db_item = create_item(db, item , user_id= token_payload.sub)
    print(db_item)
    return db_item

@router.get("")
async def test_item(db: db_dependency, skip: int = 0, limit: int = 100, token_data: Token = Depends(check_request_token)):
    db_items = get_items_by_user_id(db, token_data["sub"], skip, limit)
    return db_items