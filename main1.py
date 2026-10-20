from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="FastAPI Demo",
    version="1.0.0",
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "obsidian"},
        "displayRequestDuration": True,
        "filter": True,
        "operationsSorter": "method",
    },
)

Path("static").mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", tags=["1. Что такое FastAPI"])
def root():
    return {"message": "Hello FastAPI!"}


class Item(BaseModel):
    name: str
    price: float


@app.get("/hello", tags=["2. Класс FastAPI и обработка запроса"])
def hello(name: str = "мир"):
    return {"message": f"Привет, {name}!"}


@app.post("/items", tags=["2. Класс FastAPI и обработка запроса"])
def create_item(item: Item):
    return {"created": item.model_dump()}


@app.get("/text", tags=["3. Отправка ответа"])
def text_response():
    return "Простой текстовый ответ"


@app.get("/download", tags=["4. Отправка файлов с сервера"])
def download():
    return FileResponse("static/hello.txt", filename="hello.txt")


@app.get("/users/example/{user_id}", tags=["5. Параметры пути"])
def example_path_param(user_id: int):
    return {"user_id": user_id, "type": "int"}


@app.get("/files/{file_path:path}", tags=["5. Параметры пути"])
def example_path_convert(file_path: str):
    return {"file_path": file_path}


class UserIn(BaseModel):
    name: str
    email: EmailStr
    age: int


class User(UserIn):
    id: int


class UserPatch(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = None


users_db: dict[int, User] = {}
counter = {"id": 0}


@app.get("/users", response_model=list[User], tags=["Users CRUD"])
def list_users():
    return list(users_db.values())


@app.get("/users/{user_id}", response_model=User, tags=["Users CRUD"])
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    return users_db[user_id]


@app.post("/users", response_model=User, status_code=201, tags=["Users CRUD"])
def create_user(data: UserIn):
    if any(u.email == data.email for u in users_db.values()):
        raise HTTPException(400, "Email already exists")
    counter["id"] += 1
    user = User(id=counter["id"], **data.model_dump())
    users_db[user.id] = user
    return user


@app.put("/users/{user_id}", response_model=User, tags=["Users CRUD"])
def update_user(user_id: int, data: UserPatch):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    current = users_db[user_id]
    updated = current.model_copy(update=data.model_dump(exclude_unset=True))
    users_db[user_id] = updated
    return updated


@app.delete("/users/{user_id}", status_code=204, tags=["Users CRUD"])
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    del users_db[user_id]