FROM python:3.11-slim

# чтобы python не буферизовал stdout — логи сразу видны в docker logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# системные зависимости для psycopg2-binary
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# потом код
COPY . .

EXPOSE 5001

# команда по умолчанию переопределяется в docker-compose,
# но на всякий случай пусть будет здесь
CMD ["gunicorn", "-b", "0.0.0.0:5001", "run:app"]