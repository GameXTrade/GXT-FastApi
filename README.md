# GameXTrade [Backend API](https://v2202405172564268947.bestsrv.de/docs)

## How To run localy

### Edit Dockerfile

comment or delete this out

```markdown
ARG SECRET_KEY_VAR
ARG EMAIL_HOST_USER_VAR
ARG EMAIL_HOST_PASSWORD_VAR

ENV SECRET_KEY=$SECRET_KEY_VAR \
    EMAIL_HOST_USER=$EMAIL_HOST_USER_VAR \
 EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD_VAR \
    GOOGLE_SERVICE_ACCOUNT_JSON=$GOOGLE_SERVICE_ACCOUNT_JSON
```

like

```markdown
FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade pip -r /code/requirements.txt

#ARG SECRET_KEY_VAR
#ARG EMAIL_HOST_USER_VAR
#ARG EMAIL_HOST_PASSWORD_VAR

#ENV SECRET_KEY=$SECRET_KEY_VAR \

# EMAIL_HOST_USER=$EMAIL_HOST_USER_VAR \

# EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD_VAR \

# GOOGLE_SERVICE_ACCOUNT_JSON=$GOOGLE_SERVICE_ACCOUNT_JSON

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create a docker-compose.yml

```markdown
services:
fastapi:
build:
context: .
image: fastapi:latest
ports: - "8000:8000"
environment:
DATABASE_URL: postgresql://<PostgresUsername>:<PostgresUserPassword>@postgres:5432/<YourPostgresDatabase>
SECRET_KEY: <YOUR_JSON_WEB_TOKEN_SECRET>
depends_on: - postgres
networks: - webnet

postgres:
container_name: postgres
image: postgres:latest
environment:
POSTGRES_USER: <PostgresUsername>
POSTGRES_PASSWORD: <PostgresUserPassword>
POSTGRES_DB: fastapi
ports: - "5433:5432"
volumes: - <PathWhereToStoreDatabase>:/var/lib/postgresql/data
networks: - webnet

networks:
webnet:
```
