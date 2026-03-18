# FROM python:3.10

# WORKDIR /app

# COPY backend /app/backend

# RUN pip install --upgrade pip

# RUN pip install -r backend/requirements.txt

# WORKDIR /app/backend

# EXPOSE 8002

# CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8002"]
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r backend/requirements.txt

# Download embedding model during build
# RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

WORKDIR /app/backend

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8002"]