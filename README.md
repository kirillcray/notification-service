# notification-service

## Описание
REST API для приёма заявок на отправку уведомлений (email / telegram / sms) и их асинхронной обработки.
Запрос на создание сразу попадает в БД и публикуется в очередь RabbitMQ. Воркер забирает сообщение из очереди и отправляет уведомление (пишет в лог), обновляя статус в БД.

## Стек
- Python 3.11
- Flask
- PostgreSQL 16
- RabbitMQ 3
- SQLAlchemy + Alembic (миграции)
- pika (клиент RabbitMQ)
- Docker + docker-compose

## Запуск приложения

### 1. Клонирование репозитория

```bash
git clone https://github.com/kirillcray/notification-service
```

### 2. Создание .env

```bash
cp .env.example .env
```

### 3. Запуск докер компоус
```bash
docker-compose up --build
```
После запустятся 4 контейнера:

- Api: порт 5001

- Postgres: порт 5432

- RabbitMQ: порты 5672 и 15672 (UI)

- Worker

## Эндпоинты
- POST http://localhost:5001/api/v1/notifications создать уведомление

- GET http://localhost:5001/api/v1/notifications/id получить конкретное уведомление

- GET http://localhost:5001/api/v1/notifications/ получить список всех уведомлений

## Премеры curl запросов

### Отправка уведомления на email

```bash
curl -X POST http://localhost:5001/api/v1/notifications \
-H "Content-Type: application/json" \
-d '{
"type": "email",
"recipient": "test@example.com",
"subject": "Привет",
"message": "Тестовое сообщение"
}'
```

### Отправка уведомления на telegram

```bash
curl -X POST http://localhost:5001/api/v1/notifications \
-H "Content-Type: application/json" \
-d '{
"type": "telegram",
"recipient": "@example",
"message": "Тестовое сообщение"
}'
```
### Отправка уведомления на sms

```bash
curl -X POST http://localhost:5001/api/v1/notifications \
-H "Content-Type: application/json" \
-d '{
"type": "sms",
"recipient": "+71111111111",
"message": "Тестовое сообщение"
}'
```


### пример ответа:

Ответ при успехе
```bash
status 201 Created
{
    "id": "7fdb57a9-f99e-48f8-8678-3afac1dc5746",
    "status": "queued"
}
```
Ответы при некорректности данных
```bash
status 400 Bad request
{
    "error": "Invalid tg username"
}

{
    "error": "Invalid phone number"
}

{
    "error": "Invalid email format"
}
```



### Получить статус уведомления

```bash
curl http://localhost:5001/api/v1/notifications/<id>
```
### пример ответа:

Ответ при успехе
```bash
status 200 Ok
{
    "error": null,
    "id": "ffb3e32c-e48f-484c-9bc6-fdddd35fb17c",
    "status": "sent"
}
```
Ответ на запрос по несуществующему ID
```bash
status 404 NOT FOUND
{
    "error": "Not found"

}
```
### Список уведомлений
```bash
curl "http://localhost:5001/api/v1/notifications?status=sent&limit=10&offset=0"
```

Параметры `status`, `limit`, `offset` — опциональные.

### пример ответа:

Ответ при успехе
```bash
status 200 Ok
{
    "items": [
        {
            "channel_data": null,
            "created_at": "2026-05-25T21:00:04.745109",
            "error_text": null,
            "id": "8c318b66-f529-4479-ae84-1e0ed1b8d7cf",
            "message": "hello",
            "recipient": "test@test.ru",
            "status": "queued",
            "subject": null,
            "type": "email",
            "updated_at": "2026-05-25T21:00:04.745162"
        },
    
...
    ],
    "limit": 10,
    "offset": 0,
    "total": 18
}
```
## Тесты

### Локально

1. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   ```

2. Активируйте его:
   ```bash
   # Windows
   source venv\Scripts\activate

   # Linux / macOS
   source venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустите тесты:
   ```bash
   pytest
   ```


### Через Docker

```bash
docker-compose run --rm api pytest
```
### Postman

В папке `postman/` лежит готовая коллекция для Postman — `notification-service.postman_collection.json`.

Коллекция включает 7 запросов:
- Создание уведомления для SMS
- Создание уведомления для Email
- Создание уведомления для Telegram
- Получение конкретного уведомления (SMS, Email, Telegram)
- Получение списка всех уведомлений
## Архитектура

- API кладёт `id` уведомления в очередь и сразу отвечает клиенту.
- Worker — отдельный процесс, который слушает очередь, обрабатывает сообщения и обновляет статус в БД.

## Структура проекта

```
app/
├── api/              # эндпоинты
├── utils/            # валидаторы
├── broker.py         # publisher для RabbitMQ
├── tasks.py          # логика отправки + handle_notification
├── models.py         # модель Notification
├── config.py         # конфигурация
└── extensions.py     # db, migrate
tests/                # тесты
run.py                # точка входа для API
worker.py             # точка входа для воркера
Dockerfile
docker-compose.yml```

