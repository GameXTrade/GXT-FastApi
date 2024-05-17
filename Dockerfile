
FROM python:3.12-slim

WORKDIR /code

ARG POSTGRESQL_URL_VAR
ARG SECRET_KEY_VAR
ARG EMAIL_HOST_USER_VAR
ARG EMAIL_HOST_PASSWORD_VAR

ENV POSTGRESQL_URL=$POSTGRESQL_URL_VAR\
    SECRET_KEY=$SECRET_KEY_VAR \
    EMAIL_HOST_USER=$EMAIL_HOST_USER_VAR \
    EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD_VAR


COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt psycopg2-binary

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
