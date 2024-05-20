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
    wearable: int
    price: float

    # download_count: int

class ItemCreate(Item):
    ...