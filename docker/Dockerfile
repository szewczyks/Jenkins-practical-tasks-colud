FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Jeśli dodałeś wsgi.py:
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

# — albo — bez wsgi.py:
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--factory", "app:create_app"]
