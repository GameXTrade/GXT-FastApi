from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hashedpassword = Column(String)
    image = Column(String, default="")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    is_verified = Column(Boolean, default=False)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    
    item_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    item_type = Column(Integer)
    item_subtype = Column(Integer)
    antiflag = Column(Integer)
    
    image_link = Column(String)
    download_link = Column(String)

    price = Column(Numeric(precision=10, scale=2), nullable=False, default=0.00)

    download_count = Column(Integer, nullable=False, default = 0)
    views = Column(Integer, nullable=False, default = 0)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    status = Column(Boolean, default=False)

    owner = relationship("User", back_populates="items") 
    downloads = relationship("Download", back_populates="item")

class Download(Base):
    __tablename__ = "downloads"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)

    referer_url = Column(String, nullable=True)
    browser = Column(String, nullable=True)

    client = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    download_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    item = relationship("Item", back_populates="downloads")