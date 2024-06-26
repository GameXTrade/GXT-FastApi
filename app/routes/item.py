from fastapi import APIRouter, Depends, Request, Response, status
from pydantic import BaseModel
from app.operations.token import Token, check_request_token
from app.schemas.item_schema import ItemCreate, DownloadEntrie
from app.operations.items import (
    create_item,
    get_items_by_user_id,
    get_all_items,
    get_10_recently_added_items,
    get_item_by_id,
    get_10_notable_items,
    get_10_most_downloaded_items_for_day,
    update_downloadcount,
    insert_into_downloads,
    get_user_item2
)

from app.database.db import db_dependency

# only when payload is no used
# from app.operations.auth import authenticate_route


from fastapi_limiter.depends import RateLimiter


router = APIRouter(
    prefix="/item", 
    tags=['item']
)


@router.get("/all", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def get_items(db: db_dependency, request: Request, skip: int = 0, limit: int = 100):
    """
    Retrieve all items.

    Fetch all items from the database with optional pagination. This route is useful for retrieving a large list of items.

    Parameters:
    - skip (int, optional): The number of items to skip before starting to collect the result set. Default is 0.
    - limit (int, optional): The maximum number of items to return. Default is 100.

    Request Example:
    GET /item/all?skip=0&limit=100

    Responses:
    - 200 OK: Returns a list of items.
    - default: An error message if the request fails.
    """
    client_host = request.client.host
    # print(client_host)
    db_items = get_all_items(db, skip, limit)
    return db_items


@router.get("/recent", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def ten_recently_added_items(db: db_dependency, request: Request):
    """
    Retrieve the 10 most recently added items.

    Fetch the 10 most recently added items from the database. This route is useful for getting the latest items.

    Request Example:
    GET /item/recent

    Responses:
    - 200 OK: Returns a list of the 10 most recently added items.
    - default: An error message if the request fails.
    """
    # client_host = request.client.host
    return get_10_recently_added_items(db)

@router.get("/notables", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def ten_top_notable_items(db: db_dependency, request: Request):
    return get_10_notable_items(db)

@router.get("/top_downloaded_day", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def ten_top_downloaded_in_day(db: db_dependency, request: Request):
    return get_10_most_downloaded_items_for_day(db)

@router.get("/{item_id}", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def get_item(db: db_dependency, item_id:int, request: Request):
    """
    Retrieve an item by its ID.

    Fetch a single item from the database by its ID. This route is useful for retrieving details of a specific item.

    Parameters:
    - item_id (int, required): The ID of the item to retrieve.

    Request Example:
    GET /item/1

    Responses:
    - 200 OK: Returns the item with the specified ID.
    - 404 Not Found: If the item with the specified ID does not exist.
    - default: An error message if the request fails.
    """
    item = get_item_by_id(db, item_id)
    if item is None:
        return {"error": "Item not found"}
    return item


@router.post("/create", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def add_item_to_db(
    db: db_dependency, 
    item: ItemCreate, 
    token_data: Token = Depends(check_request_token)
):
    """
    Create a new item.

    Add a new item to the database. This route requires authentication and the payload for the new item.

    Parameters:
    - item (ItemCreate, required): The data for the new item.
    - token_data (Token, required): The token data for authentication.

    Request Body Example:
    {
      "name": "New Item",
      "description": "Description of the new item",
      "price": 100.0
    }

    Responses:
    - 201 Created: Returns the created item.
    - 401 Unauthorized: If the user is not authenticated.
    - default: An error message if the request fails.
    """
    token_payload = Token(**token_data) 
 
    db_item = create_item(db, item, user_id= token_payload.sub)
    return db_item

@router.get("")
async def get_user_items(
    db: db_dependency, 
    skip: int = 0, 
    limit: int = 100, 
    token_data: Token = Depends(check_request_token)
):
    """
    Retrieve items for the authenticated user.

    Fetch items from the database that belong to the authenticated user, with optional pagination. This route is useful for users to see their own items.

    Parameters:
    - skip (int, optional): The number of items to skip before starting to collect the result set. Default is 0.
    - limit (int, optional): The maximum number of items to return. Default is 100.
    - token_data (Token, required): The token data for authentication.

    Request Example:
    GET /item?skip=0&limit=100

    Responses:
    - 200 OK: Returns a list of the user's items.
    - 401 Unauthorized: If the user is not authenticated.
    - default: An error message if the request fails.
    """
    db_items = get_items_by_user_id(db, user_id=token_data["sub"], skip=skip, limit=limit)
    return db_items



@router.post("/download_count/{item_id}", dependencies=[Depends(RateLimiter(times=1, seconds=1))])
async def increment_download_count(db: db_dependency, item_id:int, request: Request):
    client_ip = request.headers.get('X-Forwarded-For')
    if client_ip:
        # Falls mehrere IP-Adressen im Header vorhanden sind, die erste IP-Adresse ist die tatsächliche IP-Adresse des Nutzers
        client_ip = client_ip.split(",")[0]
    else:
        client_ip = request.client.host
        
    download_model = DownloadEntrie(
        item_id = item_id, 
        client = client_ip,
        referer_url = request.headers.get('referer'),
        browser = request.headers.get('user-agent')
    )
    # ADD download entrie in downloads table
    insert_into_downloads(db, download_model)
    # SUMM all entries from download table and save it to item.download_count
    update_downloadcount(db, item_id)
    return Response(status_code = status.HTTP_200_OK)


@router.get("/getuser_items")
async def test(db: db_dependency, user_id: int):
    return get_user_item2(db, user_id)