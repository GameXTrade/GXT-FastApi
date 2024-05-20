# routes
from app.routes.item import router as item_router
from app.routes.user import router as user_router
# from app.routes.mailer import router as mail_route
# from app.routes.game import router as game_router
from app.routes.token import router as token_router

# # database models
from app.database.db import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager

def reset_sequences(db: Session):
    """
    Diese Funktion setzt die Primärschlüssel-Sequenzen auf den maximalen Wert in den entsprechenden Tabellen zurück.
    Beugt Fehlern wie psycopg2.errors.UniqueViolation vor.
    """
    tables_and_sequences = [
        ("items", "item_id", "items_item_id_seq"),
        ("users", "id", "users_id_seq")
    ]
    
    for table, column, sequence in tables_and_sequences:
        max_id_result = db.execute(text(f"SELECT MAX({column}) FROM {table}"))
        max_id = max_id_result.scalar()

        if max_id is not None:
            db.execute(text(f"ALTER SEQUENCE {sequence} RESTART WITH {max_id + 1}"))
            db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        reset_sequences(db)
        yield
    finally:
        db.close()

app = FastAPI(lifespan=lifespan)


Base.metadata.create_all(bind = engine)

origins = [
    'https://gxt-mu.vercel.app',  
    'http://localhost:5173',
]

# able to communicate with localhost apps
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
) 


app.include_router(user_router)
# app.include_router(mail_route)
app.include_router(item_router)
# app.include_router(game_router)
app.include_router(token_router)


@app.get("/",tags=["Server"])
def index():
    return {"Server is running": "version 0.1.0"}
