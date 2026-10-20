# FastAPI Demo

5 статей Metanit + CRUD users через Swagger UI.

## Запуск

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Ручки

| Тег | URL |
|---|---|
| 1. Что такое FastAPI | `GET /` |
| 2. Класс FastAPI и обработка запроса | `GET /hello`, `POST /items` |
| 3. Отправка ответа | `GET /text` |
| 4. Отправка файлов с сервера | `GET /download` |
| 5. Параметры пути | `GET /users/example/{id}`, `GET /files/{path:path}` |
| Users CRUD | `GET/POST/PUT/DELETE /users` |

## Swagger

Настройка через `swagger_ui_parameters` в `main.py`.

Документация: https://fastapi.tiangolo.com/how-to/configure-swagger-ui/

## Пример

`POST /users`:
```json
{"name": "Ivan", "email": "ivan@example.com", "age": 25}
```

`PUT /users/1`:
```json
{"age": 26}
```