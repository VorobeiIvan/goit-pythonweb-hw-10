from phonenumbers import parse, is_valid_number, NumberParseException


def validate_phone_number(value: str) -> str:
    """
    Перевіряє, чи є номер телефону валідним.

    Args:
        value (str): Номер телефону.

    Returns:
        str: Валідований номер телефону.

    Raises:
        ValueError: Якщо номер телефону некоректний або має неправильний формат.
    """
    try:
        parsed_number = parse(value, None)
        if not is_valid_number(parsed_number):
            raise ValueError("Некоректний номер телефону")
    except NumberParseException:
        raise ValueError("Некоректний формат номера телефону")

    return value
