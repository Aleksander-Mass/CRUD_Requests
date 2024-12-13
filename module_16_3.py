from fastapi import FastAPI, Path
from typing import Annotated

# Создаем приложение
app = FastAPI()

# Словарь пользователей
users = {'1': 'Имя: Example, возраст: 18'}

# 1. GET запрос для получения всех пользователей
@app.get("/users")
async def get_users() -> dict:
    return users

# 2. POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}")
async def add_user(
    username: Annotated[
        str,
        Path(
            title="Enter username",
            min_length=5,
            max_length=20,
            description="Имя пользователя должно содержать от 5 до 20 символов",
            example="UrbanUser"
        )
    ],
    age: Annotated[
        int,
        Path(
            title="Enter age",
            ge=18,
            le=120,
            description="Возраст должен быть числом от 18 до 120",
            example=24
        )
    ]
):
    new_id = str(max(map(int, users.keys())) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"User {new_id} is registered"}

# 3. PUT запрос для обновления данных пользователя
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[
        str,
        Path(
            title="Enter User ID",
            description="ID пользователя должен существовать в словаре",
            example="1"
        )
    ],
    username: Annotated[
        str,
        Path(
            title="Enter username",
            min_length=5,
            max_length=20,
            description="Имя пользователя должно содержать от 5 до 20 символов",
            example="UrbanProfi"
        )
    ],
    age: Annotated[
        int,
        Path(
            title="Enter age",
            ge=18,
            le=120,
            description="Возраст должен быть числом от 18 до 120",
            example=28
        )
    ]
):
    if user_id in users:
        users[user_id] = f"Имя: {username}, возраст: {age}"
        return {"message": f"User {user_id} has been updated"}
    return {"error": f"User {user_id} does not exist"}

# 4. DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}")
async def delete_user(
    user_id: Annotated[
        str,
        Path(
            title="Enter User ID",
            description="ID пользователя должен существовать в словаре",
            example="2"
        )
    ]
):
    if user_id in users:
        del users[user_id]
        return {"message": f"User {user_id} has been deleted"}
    return {"error": f"User {user_id} does not exist"}

# uvicorn main:app --reload