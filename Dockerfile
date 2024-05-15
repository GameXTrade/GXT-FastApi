
FROM python:3.12-slim

WORKDIR /code

ENV POSTGRESQL_URL=postgresql://root:zWNxnlcnBk96ZLsBeJ7Ob5EO5zmDeK35@dpg-coe1jji0si5c7399c4a0-a.oregon-postgres.render.com/fastapi_4g69 \
    SECRET_KEY=WW3RXUHPWHUMI7737WMW6T43CUIP2P4I \
    ALGORITHM=HS256 \
    EMAIL_HOST=smtp.gmail.com \
    EMAIL_HOST_USER=auto.emailer.001@gmail.com \
    EMAIL_HOST_PASSWORD='byeu jccv zyhu psgf'\
    EMAIL_PORT=587\
    EMAIL_USE_TLS=True\
    EMAIL_USE_SSL=False



COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
