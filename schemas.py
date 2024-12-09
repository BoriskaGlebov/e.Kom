import re
from typing import Dict, Any
from config import logger
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, field_validator, constr
import phonenumbers
from datetime import date, datetime


class SInputData(BaseModel):
    name: str = Field(...)  # Обязательное поле
    # Используем Dict для хранения динамических полей
    extra_fields: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('extra_fields', mode='before')
    def validate_extra_fields(cls, value):
        if not isinstance(value, dict):
            raise ValueError("extra_fields должно быть словарем")

        for field_name, field_value in value.items():
            if not isinstance(field_value, str):
                raise ValueError(f'Поле "{field_name}" должно быть строкой')

        return value

    def replace_data(self):
        out_dict = {"name": self.name}
        for field_name, field_value in self.extra_fields.items():
            if isinstance(field_value, str):
                if '@' in field_value and EmailStr._validate(field_value):
                    out_dict[field_name] = "email"
                elif re.match(r'^\+?\d{10,15}$', field_value):
                    try:
                        parsed_number = phonenumbers.parse(field_value)
                        if not phonenumbers.is_valid_number(parsed_number):
                            logger.error(f'Номер телефона "{field_value}" недействителен')
                            out_dict[field_name] = "text"
                            continue
                        out_dict[field_name] = "phone"
                    except phonenumbers.NumberParseException:
                        raise ValueError(f'Неверный формат номера телефона "{field_value}"')
                elif re.match(r'^\d{2}\.\d{2}\.\d{4}$', field_value) or re.match(r'^\d{4}-\d{2}-\d{2}$',
                                                                                 field_value):
                    out_dict[field_name] = 'date'
                else:
                    out_dict[field_name] = 'text'
        return out_dict

    # class Config:
    #     arbitrary_types_allowed = True
    # @field_validator('*', mode='before')
    # @classmethod
    # def validate_fields(cls, value: Any, values: Dict[str, Any], field) -> Any:
    #     if field.name != 'name':
    #         if isinstance(value, str):
    #             return "Текст"  # Текстовое поле
    #         elif isinstance(value, str) and '@' in value:
    #             return "Email" if EmailStr.validate(value) else "NO EMAIL"  # Проверка на email
    #         elif isinstance(value, str) and len(value) == 10 and value.isdigit():
    #             if phonenumbers.parse(value):
    #                 return "ТЕлефон"
    #         elif isinstance(value, str):  # Проверка на дату
    #             # Проверка формата DD.MM.YYYY
    #             if re.match(r'^\d{2}\.\d{2}\.\d{4}$', value):
    #                 return value
    #             # Проверка формата YYYY-MM-DD
    #             elif re.match(r'^\d{4}-\d{2}-\d{2}$', value):
    #                 return value
    #             else:
    #                 raise ValueError('Дата должна быть в формате DD.MM.YYYY или YYYY-MM-DD')
    #
    #         else:
    #             raise ValueError(f"{field.name} должно быть строкой, email или номером телефона")
    #     return value


#

# class SFormTemplateAdd(BaseModel):
#     name: str = ...
#     fields: Dict[str, str]  # Словарь для хранения полей с их типами
#
#     @field_validator('fields')
#     @classmethod
#     def validate_fields(cls, v):
#         allowed_types = {'email', 'phone', 'date', 'text'}
#         for field_name, field_type in v.items():
#             if field_type not in allowed_types:
#                 raise ValueError(
#                     f"Field '{field_name}' has an invalid type '{field_type}'. Allowed types are {allowed_types}.")
#         return v
#
# class SFormTemplate(BaseModel):
#     id:str
#     name: str = ...
#     fields: Dict[str, str]  # Словарь для хранения полей с их типами
#
#     @field_validator('fields')
#     @classmethod
#     def validate_fields(cls, v):
#         allowed_types = {'email', 'phone', 'date', 'text'}
#         for field_name, field_type in v.items():
#             if field_type not in allowed_types:
#                 raise ValueError(
#                     f"Field '{field_name}' has an invalid type '{field_type}'. Allowed types are {allowed_types}.")
#         return v
#
#
# class SFormsTemplateAdd(BaseModel):
#     name: str = Field(default="test_form", min_length=3)
#     email: EmailStr = Field(default='user@mail.ru')
#     phone: str = Field(default='+79852000338')  # Валидация номера телефона с помощью регулярного выражения
#     date_form: str = Field(default='01.01.2024')
#
#     @field_validator('phone')
#     @classmethod
#     def validate_phone_number(cls, value):
#         try:
#             parsed_number = phonenumbers.parse(value)
#             if not phonenumbers.is_valid_number(parsed_number):
#                 raise ValueError('Номер телефона недействителен')
#             return value
#         except phonenumbers.NumberParseException:
#             raise ValueError('Неверный формат номера телефона')
#
#     @field_validator('date_form')
#     @classmethod
#     def validate_date_format(cls, value):
#         # Проверка формата DD.MM.YYYY
#         if re.match(r'^\d{2}\.\d{2}\.\d{4}$', value):
#             return value
#         # Проверка формата YYYY-MM-DD
#         elif re.match(r'^\d{4}-\d{2}-\d{2}$', value):
#             return value
#         else:
#             raise ValueError('Дата должна быть в формате DD.MM.YYYY или YYYY-MM-DD')
#
#
# class SFormsTemplate(BaseModel):
#     id: str
#     name: str = Field(default="test_form", min_length=3)
#     email: EmailStr = Field(default='user@mail.ru')
#     phone: str = Field(default='+79852000338')  # Валидация номера телефона с помощью регулярного выражения
#     date_form: str = Field(default='01.01.2024')
#
#     @field_validator('phone')
#     @classmethod
#     def validate_phone_number(cls, value):
#         try:
#             parsed_number = phonenumbers.parse(value)
#             if not phonenumbers.is_valid_number(parsed_number):
#                 raise ValueError('Номер телефона недействителен')
#             return value
#         except phonenumbers.NumberParseException:
#             raise ValueError('Неверный формат номера телефона')
#
#     @field_validator('date_form')
#     @classmethod
#     def validate_date_format(cls, value):
#         # Проверка формата DD.MM.YYYY
#         if re.match(r'^\d{2}\.\d{2}\.\d{4}$', value):
#             return value
#         # Проверка формата YYYY-MM-DD
#         elif re.match(r'^\d{4}-\d{2}-\d{2}$', value):
#             return value
#         else:
#             raise ValueError('Дата должна быть в формате DD.MM.YYYY или YYYY-MM-DD')
#
#     class Config:
#         # Позволяет Pydantic работать с ObjectId из MongoDB
#         json_encoders = {
#             ObjectId: str  # Преобразование ObjectId в строку
#         }
#         # allow_population_by_field_name = True  # Позволяет использовать alias


if __name__ == '__main__':
    # test = SFormsTemplateAdd(name="dsss", email='pfd@mail.ru', phone='+7 (985) 200 03 38', date_form='01.01.2023')
    # print(test)
    # print(test.model_dump())
    data_fields = {
        "name": "somename",
        "email_user": "example@mail.ru",
        "user_phone": "+798520003338",
        "birthday": "2000-01-01"
    }
    some = SInputData(name=data_fields.get('name'), extra_fields={k: v for k, v in data_fields.items() if k != "name"})
    print(some.model_dump())
    print(some.replace_data())

    # def validation(val_form: SInputData):
    #     check_dict = val_form.model_dump()
    #     for k, v in check_dict.items():
    #         print(k, v)
    #         if k == "name":
    #             print(some.validate_fields(v, k))
    #             continue
    #         for key, value in v.items():
    #             print(key, value)
    #             print(some.validate_fields(value, key))
    #
    #
    # validation(some)
