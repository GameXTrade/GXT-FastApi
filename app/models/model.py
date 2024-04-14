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
    is_active = Column(Boolean, default=False)

    items = relationship("Item", back_populates="owner")

# class Metin2Items(Base):
#     __tablename__ = "metin2_items"

#     id = Column(Integer, primary_key=True)
#     game_id = Column(Integer, ForeignKey("games.id"), nullable=False)

#     description = Column(String, index=True)
#     link = Column(String)


#     item_name = Column(String)
#     item_type = Column(Integer)
#     sub_type = Column(Integer)
#     anti_flag = Column(Integer)
#     item_wear = Column(Integer)

#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

#     owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # owner = relationship("User", back_populates="metin2_items")

class Item(Base):
    __tablename__ = "items"
    
    item_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String, index=True)
    link = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="items") 

