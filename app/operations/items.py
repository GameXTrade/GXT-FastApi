from app.schemas.item_schema import ItemCreate, DownloadEntrie
from app.models import model
from sqlalchemy.orm import Session
from sqlalchemy import desc, text, and_,func
from pydantic import BaseModel
from datetime import datetime, timedelta, date

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

def get_10_most_downloaded_items_for_day(db: Session):
    # Start des heutigen Tages (00:00:00)
    start_of_day = datetime.combine(date.today(), datetime.min.time())
    
    # Ende des aktuellen Zeitpunkts
    end_of_day = datetime.now()

    query = db.query(model.Item, model.User.username, func.count(model.Download.id).label('download_count')) \
        .join(model.User, model.Item.owner_id == model.User.id) \
        .outerjoin(model.Download, and_(
            model.Download.item_id == model.Item.item_id,
            model.Download.download_timestamp >= start_of_day,
            model.Download.download_timestamp <= end_of_day
        )) \
        .filter(model.Item.status == True) \
        .group_by(model.Item.item_id, model.User.username) \
        .order_by(desc(func.count(model.Download.id))) \
        .limit(10) \
        .all()
    
    results = []
    for item, username, download_count in query:
        item_dict = item.__dict__
        item_dict['owner_name'] = username
        item_dict['download_count'] = download_count
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

def update_downloadcount(db: Session, item_id: int) -> None:
    item = db.query(model.Item).filter(model.Item.item_id == item_id).first()
    if item:
        download_count = db.query(model.Download).filter(model.Download.item_id == item_id).count()
        item.download_count = download_count
        db.commit()

def insert_into_downloads(db: Session, download_model: DownloadEntrie):
    download_item = model.Download(
        item_id = download_model.item_id, 
        client = download_model.client,
        referer_url = download_model.referer_url,
        browser = download_model.browser
)
    db.add(download_item)
    db.commit()
    db.refresh(download_item)

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