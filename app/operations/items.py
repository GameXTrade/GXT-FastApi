from app.schemas.item_schema import ItemCreate
from app.models import model
from sqlalchemy.orm import Session
from sqlalchemy import desc, text, and_
from pydantic import BaseModel
from datetime import datetime, timedelta

def get_items_by_user_id(db:Session, user_id: int, skip: int = 0, limit: int = 100):   
    return db.query(model.Item).filter(model.Item.owner_id == user_id).offset(skip).limit(limit).all()

def get_10_recently_added_items(db:Session):
    query = db.query(model.Item, model.User.username).\
            join(model.User, model.Item.owner_id == model.User.id).\
            filter(model.Item.status == True).\
            order_by(desc(model.Item.created_at)).limit(10).all()
    results = []
    for item, username in query:
        item_dict = item.__dict__
        item_dict['owner_name'] = username
        results.append(item_dict)

    return results

def get_10_notable_items(db:Session):
    query = db.query(model.Item, model.User.username) \
        .join(model.User, model.Item.owner_id == model.User.id) \
        .filter(model.Item.status == True) \
        .order_by(desc(model.Item.views), model.Item.download_count) \
        .limit(10) \
        .all()
    
    results = []
    for item, username in query:
        item_dict = item.__dict__
        item_dict['owner_name'] = username
        results.append(item_dict)

    return results

def get_10_most_downloaded_items_for_day(db:Session):

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    query = db.query(model.Item, model.User.username) \
        .join(model.User, model.Item.owner_id == model.User.id) \
        .filter(model.Item.status == True) \
        .filter(and_(
            model.Item.created_at >= start_of_day,
            model.Item.created_at < end_of_day
        )) \
        .order_by(desc(model.Item.download_count)) \
        .limit(10) \
        .all()
    
    results = []
    for item, username in query:
        item_dict = item.__dict__
        item_dict['owner_name'] = username
        results.append(item_dict)

    return results

def get_item_by_id(db: Session, item_id: int):
    query = db.query(model.Item, model.User.username).\
        join(model.User, model.Item.owner_id == model.User.id).\
        filter(model.Item.item_id == item_id)
    
    results = []
    for item, username in query:
        item.views += 1
        item_dict = item.__dict__.copy()
        item_dict['owner_name'] = username
        results.append(item_dict)
    
    if results:
        db.commit() 
    
    return results

def update_downloadcount(db:Session, item_id: int)->None:
    item = db.query(model.Item).filter(model.Item.item_id == item_id).first()
    if item:
        item.download_count += 1
        db.commit()

def get_all_items(db:Session,skip: int = 0, limit: int = 100):
    query = db.query(model.Item, model.User.username).\
        join(model.User, model.Item.owner_id == model.User.id).\
        offset(skip).limit(limit).all()
    
    results = []
    for item, username in query:
        item_dict = item.__dict__
        item_dict['owner_name'] = username
        results.append(item_dict)
    
    return results

def create_item(db:Session, item: ItemCreate, user_id: int): 
    db_item = model.Item(
        
        name = item.name, 
        item_type = item.type,
        item_subtype = item.subtype,
        antiflag = item.antiflag, 

        image_link = item.imagelink, 
        download_link= item.link, 
        
        price = item.price, 
        
        download_count = 0, 
        views = 0,
        
        owner_id = user_id, 
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


class UserId(BaseModel):
    user_id: int

def get_user_item2(db:Session, user: UserId):
    result = db.execute(text(
        """
        SELECT * 
        FROM items
        JOIN users ON items.owner_id = users.id
        WHERE users.id = :user_id
        """),{"user_id": user.user_id})
    return result.fetchall()