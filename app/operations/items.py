from app.schemas.item_schema import ItemCreate
from app.models import model
from sqlalchemy.orm import Session
from sqlalchemy import desc


def get_items_by_user_id(db:Session, user_id: int, skip: int = 0, limit: int = 100):   
    return db.query(model.Item).filter(model.Item.owner_id == user_id).offset(skip).limit(limit).all()

def get_10_recently_added_items(db:Session):
    query = db.query(model.Item, model.User.username).\
            join(model.User, model.Item.owner_id == model.User.id).\
            filter(model.Item.activated == True).\
            order_by(desc(model.Item.created_at)).limit(10).all()
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
        name = item.name, antiflag = item.antiflag, 
        link= item.link, type = item.type, imagelink = item.imagelink, 
        owner_id = user_id, price = item.price, wearable = item.wearable,
        download_count = 0, views = 0
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item