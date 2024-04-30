from app.schemas.item_schema import ItemCreate
from app.models import model
from sqlalchemy.orm import Session



def get_items_by_user_id(db:Session, user_id: int, skip: int = 0, limit: int = 100):   
    return db.query(model.Item).filter(model.Item.owner_id == user_id).offset(skip).limit(limit).all()


def create_item(db:Session, item: ItemCreate, user_id: int): 
    db_item = model.Item(name = item.name, antiflag = item.antiflag, link= item.link, type = item.type, imagelink = item.imagelink, owner_id = user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item