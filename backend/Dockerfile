FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Gereksinimleri yükle
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Projeyi kopyala
COPY . .

# Django sunucusunu ayağa kaldır
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
