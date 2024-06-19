from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class Item(BaseModel):

    name: str
    type: int
    subtype: int
    antiflag: int

    imagelink: str = Field(default = '')
    link: str = Field(default = '')
    
    price: float = Field(default = 0.0)

class ItemCreate(Item):
    ...