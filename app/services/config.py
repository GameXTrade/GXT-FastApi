import os 
from dotenv import load_dotenv


load_dotenv()

# localhost Postgres
# __POSTGRESQL_USER = 'postgres'
# __POSTGRESQL_PWD = 'mysecretpassword'#'Rq9$T7W'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Postgres Host
# POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
# POSTGRESQL_USER_PASSWORD= os.getenv("POSTGRESQL_PWD")


# POSTGRESQL_PORT = 5433


POSTGRESQL_ACCESS_URL = os.getenv("DATABASE_URL")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'





