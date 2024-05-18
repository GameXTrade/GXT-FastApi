
# # routes
from app.routes.item import router as item_router
from app.routes.user import router as user_router
# from app.routes.mailer import router as mail_route
# from app.routes.game import router as game_router
from app.routes.token import router as token_router

# # database models
from app.database.db import Base, engine

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


app = FastAPI()

origins = [
    'https://gxt-mu.vercel.app/',  
    # 'http://localhost:5173',
]

# able to communicate with localhost apps
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

Base.metadata.create_all(bind = engine)


app.include_router(user_router)
# app.include_router(mail_route)
app.include_router(item_router)
# app.include_router(game_router)
app.include_router(token_router)


@app.get("/",tags=["Server"])
def index():
    return {"Server is running": "version 0.1.0"}
 