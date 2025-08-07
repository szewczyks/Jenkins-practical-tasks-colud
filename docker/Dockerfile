FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
