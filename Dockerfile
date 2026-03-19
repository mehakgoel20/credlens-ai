# FROM python:3.10-slim

# WORKDIR /app

# COPY backend/requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# # download embedding model
# RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# COPY . .

# WORKDIR /app/backend

# CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY dashboard ./dashboard

ENV PYTHONPATH=/app/backend

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]