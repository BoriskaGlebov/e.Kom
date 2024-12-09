from contextlib import asynccontextmanager
import random

from config import logger
import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field, validator, field_validator
from typing import List

from data_generate import random_data, generate_random_data
from schemas import SInputData

# Настройка подключения к MongoDB
client = AsyncIOMotorClient("mongodb://user:password@localhost:27017")
db_name = 'e_kom'
client.drop_database('ekom')
db = client[db_name]  # Имя вашей базы данных
templates_collection = db["form_templates"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Действия перед запуском приложения.

    :param app:
    :return:
    """
    logger.info("Перед первым запуском некоторые действия.")
    await client.drop_database(db_name)
    logger.info("БД очищена")
    num_fields_to_generate = random.randint(1, 10)  # Случайное количество полей от 1 до 10
    # Случайное количество полей от 1 до 10
    random_data = [generate_random_data(num_fields_to_generate) for _ in range(10)]
    print(random_data)
    await templates_collection.insert_many(random_data)
    yield
    client.close()


app = FastAPI(
    debug=True,
    title="Form API",
    summary="Web-приложение для определения заполненных форм.",
    description="""
---
# Описание
---
Это веб-приложение на **FastAPI** предназначено для обработки заполненных форм и определения соответствующих шаблонов форм на основе переданных данных. Приложение поддерживает валидацию полей и возвращает информацию о шаблонах форм.

## Основные требования

### Поддержка типов данных

Поля могут иметь следующие типы:
- **email**
- **телефон**
- **дата**
- **текст**
---
Все типы, кроме текста, должны проходить валидацию.

### Формат данных

- Телефон должен передаваться в формате `+7 xxx xxx xx xx`.
- Дата должна передаваться в формате `DD.MM.YYYY` или `YYYY-MM-DD`.

### Определение шаблона формы

Шаблон формы должен содержать уникальный набор полей с указанием их типов.

#### Пример шаблона:

```json
{
    "name": "Form template name",
    "fields": {
        "field_name_1": "email",
        "field_name_2": "phone"
    }
}
""",
    contact={
        "name": "Boriska Glebov",
        "url": "http://localhost:8000/docs",
        "email": "BorisTheBlade.glebov@yandex.ru",
    },
    lifespan=lifespan,
)


@app.post("/get_form", )
async def get_form(form_data: SInputData):
    print(form_data)
    return form_data.replace_data()


# @app.post("/forms/", response_model=SFormTemplate)
# async def create_item(item: SFormTemplateAdd):
#     item_dict = item.model_dump()
#     print(item_dict)
#     result = await templates_collection.insert_one(item_dict)  # Вставка документа в коллекцию
#     item_dict["id"] = str(result.inserted_id)  # Добавление ID к объекту
#     return item_dict
#
#
# @app.get("/forms/", response_model=List[SFormsTemplate])
# async def read_items():
#     items = []
#     async for item in templates_collection.find():  # Асинхронное извлечение документов
#         item["id"] = str(item["_id"])  # Преобразование ObjectId в строку
#         print(item)
#         items.append(item)
#     print(items)
#     return items


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
