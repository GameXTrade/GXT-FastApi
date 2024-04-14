from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.operations.games import CreateGame, create_game,get_game_by_name, get_games, delete_game

router = APIRouter(
    prefix="/game", 
    tags=['games']
)
# GET ALL
@router.get("")
def get_all_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    games = get_games(db, skip, limit)
    return games

# GET ONE
@router.get("/{game_name}")
def get_game(game_name:str, db: Session = Depends(get_db)):
    games = get_game_by_name(db, name=game_name)
    return games


# POST
@router.post("")
def add_game(game: CreateGame, db: Session = Depends(get_db)):
    db_game = get_game_by_name(db, name=game.name)
    if db_game:
        raise HTTPException(status_code=400, detail = "Email already registered")
    db_game = create_game(db, game)
    return db_game

# DELETE
@router.delete("/{game_name}")
def erase_game(game_name: str, db: Session = Depends(get_db)):
    result = delete_game(db, game_name)
    return {"deleted": result}