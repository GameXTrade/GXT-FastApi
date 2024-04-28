from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP
from app.database.db import Base




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    image = Column(String, default="")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    is_verified = Column(Boolean, default=False)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    
    item_id = Column(Integer, primary_key=True)
    
    name = Column(String, unique=True)
    antiflag = Column(Integer)
    link = Column(String)
    type = Column(Integer)
    imagelink = Column(String)

    # description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="items") 

