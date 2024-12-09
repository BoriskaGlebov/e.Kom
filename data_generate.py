from faker import Faker
import random

# Создаем экземпляр Faker
fake = Faker()


def generate_random_key() -> str:
    """Генерирует случайное название ключа из 1-3 слов.

    :return: Случайная строка, состоящая из 1-3 слов.
    """
    num_words = random.randint(1, 3)  # Случайное количество слов от 1 до 3
    return ' '.join(fake.words(num_words))  # Генерация случайных слов


def generate_random_data(num_fields: int) -> dict:
    """Генерирует случайные данные в виде словаря с ассоциативными ключами.

    :param num_fields: Количество полей для генерации.
    :return: Словарь, содержащий случайные ключи и значения.
    """

    # Шаблоны ключей для различных типов данных
    key_templates = {
        'email': ['email', 'email_address', 'user_email', 'contact_email'],
        'phone': ['phone', 'phone_number', 'user_phone', 'contact_phone'],
        'name': ['name', 'full_name', 'username'],
        'birthday': ['birthday', 'date_of_birth', 'dob', 'work_date', 'meet_date'],
        'text': [generate_random_key() for _ in range(4)]
    }

    # Словарь для хранения случайных данных
    data_fields = {}

    # Генерируем случайные данные для заданного количества полей
    for _ in range(num_fields):
        data_type = random.choice(list(key_templates.keys()))  # Выбираем случайный тип данных
        key = random.choice(key_templates[data_type])  # Выбираем случайный ключ из шаблонов
        data_fields['name'] = generate_random_key()

        if data_type == 'email':
            data_fields[key] = "email"  # Генерация случайного email
        elif data_type == 'phone':
            data_fields[key] = "phone"  # Генерация номера телефона
        elif data_type == 'birthday':
            data_fields[key] = "date"  # Генерация даты рождения в формате YYYY-MM-DD
        elif data_type == 'text':
            data_fields[key] = "text"  # Генерация текста

    return data_fields


if __name__ == '__main__':
    # Пример использования
    num_fields_to_generate = random.randint(1, 10)  # Случайное количество полей от 1 до 10
    random_data = generate_random_data(num_fields_to_generate)
    print(random_data)