# TODO: Harden image, run app as non root and maybe use some more minimal base image for production, prepare app for prod, disable /docs...
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]