import os 
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel


load_dotenv()

# localhost Postgres
__POSTGRESQL_USER = 'postgres'
__POSTGRESQL_PWD = 'Rq9$T7W'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Postgres Host
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_USER_PASSWORD= os.getenv("POSTGRESQL_PWD")


POSTGRESQL_PORT = 5432

# DB local
# POSTGRESQL_ACCESS_URL = f"postgresql://{__POSTGRESQL_USER}:{__POSTGRESQL_PWD}@localhost:{POSTGRESQL_PORT}/fastapi"

POSTGRESQL_ACCESS_URL = os.getenv("POSTGRESQL_URL")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'


class MailBody(BaseModel):
    to: List[str]
    subject: str
    body: str


