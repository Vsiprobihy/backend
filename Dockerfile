FROM python:3.12-slim

RUN apt-get update && apt-get install -y build-essential libpq-dev

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
