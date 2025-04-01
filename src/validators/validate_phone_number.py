from phonenumbers import parse, is_valid_number, NumberParseException


def validate_phone_number(phone_number: str) -> str:
    """
    Перевіряє валідність телефонного номера.

    :param phone_number: Номер телефону у вигляді рядка.
    :return: Валідний номер телефону у форматі E.164.
    :raises ValueError: Якщо номер телефону недійсний.
    """
    try:
        parsed_number = parse(phone_number)
        if not is_valid_number(parsed_number):
            raise ValueError(f"Недійсний номер телефону: {phone_number}")
        return phone_number
    except NumberParseException:
        raise ValueError(f"Помилка розбору номера телефону: {phone_number}")
