import re
from typing import Any, Dict

import phonenumbers
# from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator

from config import logger


class SInputDdataEmpty(BaseModel):
    """Модель для представления пустых входных данных с дополнительными полями.

    Attributes:
        extra_fields (Dict[str, Any]): Словарь для хранения дополнительных полей.
    """

    extra_fields: Dict[str, Any] = Field(default_factory=dict)


class SInputData(BaseModel):
    """Модель для представления входных данных с валидацией дополнительных полей.

    Attributes:
        extra_fields (Dict[str, Any]): Словарь для хранения дополнительных полей.

    Methods:
        replace_data() -> Dict[str, str]: Заменяет значения дополнительных полей на их типы.
    """

    extra_fields: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("extra_fields", mode="before")
    def validate_extra_fields(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация дополнительных полей.

        Проверяет, что дополнительные поля являются словарем и что все значения - строки.

        :param value: Значения дополнительных полей.
        :raises ValueError: Если значение не является словарем или если одно из значений не строка.
        :return: Проверенное значение.
        """
        if not isinstance(value, dict):
            raise ValueError("extra_fields должно быть словарем")

        for field_name, field_value in value.items():
            if not isinstance(field_value, str):
                raise ValueError(f'Поле "{field_name}" должно быть строкой')

        return value

    def replace_data(self) -> Dict[str, str]:
        """Заменяет значения дополнительных полей на их типы.

        Определяет типы данных на основе значений в `extra_fields`.

        :return: Словарь с именами полей и соответствующими типами данных.
        """
        out_dict = {}
        for field_name, field_value in self.extra_fields.items():
            if isinstance(field_value, str):
                if "@" in field_value and EmailStr._validate(field_value):
                    out_dict[field_name] = "email"
                elif re.match(r"^\+?\d{10,15}$", field_value):
                    try:
                        parsed_number = phonenumbers.parse(field_value)
                        if not phonenumbers.is_valid_number(parsed_number):
                            logger.error(
                                f'Номер телефона "{field_value}" недействителен'
                            )
                            out_dict[field_name] = "text"
                            continue
                        out_dict[field_name] = "phone"
                    except phonenumbers.NumberParseException:
                        raise ValueError(
                            f'Неверный формат номера телефона "{field_value}"'
                        )
                elif re.match(r"^\d{2}\.\d{2}\.\d{4}$", field_value) or re.match(
                    r"^\d{4}-\d{2}-\d{2}$", field_value
                ):
                    out_dict[field_name] = "date"
                else:
                    out_dict[field_name] = "text"
        return out_dict


class SFormTemplate(BaseModel):
    """Модель для представления шаблона формы.

    Attributes:
        name (str): Название шаблона формы.
        fields (Dict[str, str]): Словарь для хранения полей с их типами.

    Methods:
        validate_fields(v: Dict[str, str]) -> Dict[str, str]: Валидация типов полей шаблона.
    """

    name: str = ...
    fields: Dict[str, str]  # Словарь для хранения полей с их типами

    @field_validator("fields")
    @classmethod
    def validate_fields(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Валидация типов полей шаблона формы.

        Проверяет, что все типы полей являются допустимыми.

        :param v: Словарь с именами полей и их типами.
        :raises ValueError: Если тип поля недопустим.
        :return: Проверенное значение.
        """
        allowed_types = {"email", "phone", "date", "text"}
        for field_name, field_type in v.items():
            if field_type not in allowed_types:
                raise ValueError(
                    f"Field '{field_name}' has an invalid type '{field_type}'. Allowed types are {allowed_types}."
                )
        return v
