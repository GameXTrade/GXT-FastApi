from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class Item(BaseModel):
    name: str
    # creator: str
    antiflag: int
    link: str
    type: int
    imagelink: Optional[str] = None

class ItemCreate(Item):
    ...