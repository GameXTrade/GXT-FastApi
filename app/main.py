# routes
from app.routes.item import router as item_router
from app.routes.user import router as user_router
# from app.routes.mailer import router as mail_route
# from app.routes.game import router as game_router
# from app.routes.token import router as token_router


# # database models
from app.database.db import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI#, Request,UploadFile
from contextlib import asynccontextmanager
# from app.factory.upload_google_drive import GoogleDriveFactory


import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter

def reset_sequences(db: Session):
    """
    Reset database sequences to avoid primary key conflicts.

    This function resets the sequences for specified tables to ensure that the next value used for 
    the primary key is higher than any existing key. This is useful after a data import or manual 
    modification of the database where sequences might get out of sync.

    Parameters:
    - db (Session): The SQLAlchemy session used to execute the database commands.

    Tables and Sequences:
    - items: Resets the "items_item_id_seq" sequence based on the "item_id" column.
    - users: Resets the "users_id_seq" sequence based on the "id" column.

    Steps:
    1. For each table and sequence pair, find the current maximum value in the primary key column.
    2. If the maximum value is found, restart the sequence with the value higher than this maximum.
    3. Commit the changes to the database.

    Example:
    reset_sequences(db)
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
        print("reset_sequences method executed")
        
        redis_connection = redis.from_url("redis://redis:6379", encoding="utf8")
        await FastAPILimiter.init(redis_connection)
        print("FastAPILimiter initialized")
        yield

    finally:
        await FastAPILimiter.close()
        db.close()

app = FastAPI(lifespan=lifespan)


Base.metadata.create_all(bind = engine)

origins = [ # Setting cors origin
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
# app.include_router(token_router)


@app.get("/",tags=["Server"])
def index():
    return {"Server is running": "version 0.1.0"}

# Testing new function for uploading files in the cloud via google python Lib.
# @app.post("/upload")
# async def index(file_upload: UploadFile):
#     save_file = GoogleDriveFactory()

#     file_id = save_file.upload_file(file_upload)
#     file_url = save_file.share_file(file_id)
#     print("file_id", file_id, "filename", file_upload.filename, "file_url", file_url)
#     return {"file_id": file_id, "filename": file_upload.filename, "file_url": file_url}
