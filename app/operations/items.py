from app.schemas.item_schema import ItemCreate
from app.models import model
from sqlalchemy.orm import Session



def get_items_by_user_id(db:Session, user_id: int, skip: int = 0, limit: int = 100):   
    return db.query(model.Item).filter(model.Item.owner_id == user_id).offset(skip).limit(limit).all()

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
    db_item = model.Item(name = item.name, antiflag = item.antiflag, link= item.link, 
                         type = item.type, imagelink = item.imagelink, owner_id = user_id, price = item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item