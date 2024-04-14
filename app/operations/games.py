from app.models import model
from sqlalchemy.orm import Session
from pydantic import BaseModel

class GameBase(BaseModel):
    name: str
    description: str

class CreateGame(GameBase):
    ...

class Game(GameBase):
    id: int
    class Config:
        from_attributes = True

def get_games(db:Session, skip: int = 0, limit: int = 100):
    return db.query(model.Game).offset(skip).limit(limit).all()

def get_game_by_name(db: Session, name: str):
    return db.query(model.Game).filter(model.Game.name == name).first()

def create_game(db:Session, game: CreateGame): 
    db_game = model.Game(name = game.name, description = game.description)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def delete_game(db:Session, game_name: str):
    db_game = db.query(model.Game).filter(model.Game.name==game_name).first()
    if db_game:
        db.delete(db_game)
        db.commit()
        return True
    else:
        return False