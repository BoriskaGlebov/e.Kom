from contextlib import asynccontextmanager
import random

from fastapi.params import Depends

from config import logger
import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Union

from data_generate import generate_random_data
from schemas import SInputData, SFormTemplate, SInputDdataEmpty


# Настройка подключения к MongoDB
MONGODB_URL = "mongodb://user:password@localhost:27017"
DATABASE_NAME = 'e_kom'

# Создаем экземпляр клиента MongoDB
client = AsyncIOMotorClient(MONGODB_URL)

# Функция для получения подключения к базе данных
async def get_db():
    """Получение подключения к базе данных."""
    db = client[DATABASE_NAME]  # Получаем базу данных
    try:
        yield db  # Возвращаем подключение к базе данных
    finally:
        pass  # Здесь можно закрыть соединение, если это необходимо
# client = AsyncIOMotorClient("mongodb://user:password@localhost:27017")
# db_name = 'e_kom'
# client.drop_database('ekom')
# db = client[db_name]  # Имя вашей базы данных
# templates_collection = db["form_templates"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.

    This function performs setup actions before the application starts,
    including clearing the database and populating it with random data.

    :param app: The FastAPI application instance.
    """
    logger.info("Перед первым запуском некоторые действия.")

    await client.drop_database(DATABASE_NAME)
    logger.info("БД очищена")
    db = client[DATABASE_NAME]
    random_data = [generate_random_data(random.randint(1, 10)) for _ in range(100)]
    templates_collection = db["form_templates"]
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


@app.post("/get_form", response_model=Union[List[SFormTemplate], SInputDdataEmpty])
async def get_form(form_data: SInputData,db=Depends(get_db)) -> Union[List[SFormTemplate], SInputDdataEmpty]:
    """
    Retrieve form templates based on input data.

    This endpoint accepts form data and searches for matching templates in the database.

    :param form_data: The input data containing fields to search for.

    :return: A list of matching form templates (SFormTemplate) or an empty input response (SInputDdataEmpty)
             if no templates are found.
    """
    print(form_data)
    fields_search = form_data.replace_data()
    print(fields_search)

    templates_collection=db["form_templates"]
    res = await templates_collection.find(fields_search).to_list(length=None)
    print(res)
    if res:
        items = []
        for item in res:
            items.append(SFormTemplate(
                name=item["name"],
                fields={k: v for k, v in item.items() if k not in ('_id', 'name')}
            ))
        return items

    logger.error("Не нашлось нужного шаблона")

    return SInputDdataEmpty(extra_fields=fields_search)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)