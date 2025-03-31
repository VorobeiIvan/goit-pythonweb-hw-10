import secrets


def generate_secret_key(length: int = 32) -> str:
    """
    Генерує випадковий секретний ключ.

    Args:
        length (int): Довжина ключа в байтах. За замовчуванням 32.

    Returns:
        str: Згенерований секретний ключ у шістнадцятковому форматі.

    Як запустити:

    ```bash
    python key_generator.py
    ```
    """
    if length <= 0:
        raise ValueError("Довжина ключа повинна бути більше 0.")
    return secrets.token_hex(length)


if __name__ == "__main__":
    try:
        print("Згенерований секретний ключ:")
        print(generate_secret_key())
    except ValueError as e:
        print(f"Помилка: {e}")
