
FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade pip -r /code/requirements.txt

# ARG SECRET_KEY_VAR
# ARG EMAIL_HOST_USER_VAR
# ARG EMAIL_HOST_PASSWORD_VAR

# ENV SECRET_KEY=$SECRET_KEY_VAR \
#     EMAIL_HOST_USER=$EMAIL_HOST_USER_VAR \
#     EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD_VAR \
#     GOOGLE_SERVICE_ACCOUNT_JSON=$GOOGLE_SERVICE_ACCOUNT_JSON


COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
