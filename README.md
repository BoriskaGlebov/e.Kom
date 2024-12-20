# e.Kom
# Form API

## Описание

Это веб-приложение на **FastAPI**, предназначенное для обработки заполненных форм и определения соответствующих шаблонов форм на основе переданных данных. Приложение поддерживает валидацию полей и возвращает информацию о шаблонах форм.

### Основные требования

Поля могут иметь следующие типы:
- **email**
- **телефон**
- **дата**
- **текст**

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
```
### Установка
Для установки необходимых зависимостей выполните следующую команду:
```bash
pip install -r requirements.txt
```
### Запуск приложения с использованием Docker
Предварительные требования\
Убедитесь, что у вас установлены следующие инструменты:
* Docker
* Docker Compose
### Запуск приложения
Клонируйте этот репозиторий:
```bash
git clone <URL вашего репозитория>
cd <имя_папки_репозитория>
```

#### Постройте и запустите контейнеры с помощью Docker Compose:
```bash
docker-compose up -d --build
```

После успешного запуска приложение будет доступно по адресу http://localhost:8000.\
Вы можете получить доступ к документации API по адресу http://localhost:8000/docs, где вы найдете информацию о доступных эндпоинтах и примеры запросов.
### Остановка приложения
Чтобы остановить и удалить контейнеры, выполните команду:
```bash
docker-compose down
```


## Тестирование
Для запуска тестов используйте следующую команду:
```bash
pytest -v tests/
```
Тесты проверяют функциональность API и корректность обработки данных.\
Убедитесь, что все тесты проходят успешно перед развертыванием приложения.
## Лицензия
Этот проект лицензирован под MIT License - смотрите файл LICENSE для подробностей.
### Контакты
Если у вас есть вопросы или предложения,\
вы можете связаться со мной по электронной почте: \
**BorisTheBlade.glebov@yandex.ru.**