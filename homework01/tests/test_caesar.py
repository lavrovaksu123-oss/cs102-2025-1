def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for char in plaintext:
        # Если символ - заглавная буква
        if "A" <= char <= "Z":
            # Преобразуем букву в число: A=0, B=1, ..., Z=25
            position = ord(char) - ord("A")
            # Сдвигаем позицию и обеспечиваем цикличность (%26)
            new_position = (position + shift) % 26
            # Преобразуем обратно в букву
            new_char = chr(new_position + ord("A"))
            ciphertext += new_char

        # Если символ - строчная буква
        elif "a" <= char <= "z":
            position = ord(char) - ord("a")
            new_position = (position + shift) % 26
            new_char = chr(new_position + ord("a"))
            ciphertext += new_char

        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for char in ciphertext:
        if "A" <= char <= "Z":
            position = ord(char) - ord("A")
            # Для расшифровки вычитаем сдвиг вместо сложения
            new_position = (position - shift) % 26
            new_char = chr(new_position + ord("A"))
            plaintext += new_char

        elif "a" <= char <= "z":
            position = ord(char) - ord("a")
            new_position = (position - shift) % 26
            new_char = chr(new_position + ord("a"))
            plaintext += new_char

        else:
            plaintext += char

    return plaintext
