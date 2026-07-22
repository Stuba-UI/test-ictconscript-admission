FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask gunicorn

COPY main.py database.py seed.py data.json ./
COPY static ./static

RUN python -c "from database import init_db; init_db()" && python seed.py

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
