FROM python:3.11-slim-bookworm
WORKDIR /app

COPY . . 

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate ; python manage.py runserver 0.0.0.0:8000"]
