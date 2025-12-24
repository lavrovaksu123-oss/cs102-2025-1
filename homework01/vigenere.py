import typing as tp


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    result = []
    keyword = keyword.lower()  # Приводим ключ к нижнему регистру для единообразия
    key_len = len(keyword)

    for i, char in enumerate(plaintext):
        if "a" <= char <= "z":
            shift = ord(keyword[i % key_len]) - ord("a")
            result.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= char <= "Z":
            shift = ord(keyword[i % key_len].upper()) - ord("A")
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        else:
            result.append(char)

    return "".join(result)


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    result = []
    keyword = keyword.lower()  # Приводим ключ к нижнему регистру для единообразия
    key_len = len(keyword)

    for i, char in enumerate(ciphertext):
        if "a" <= char <= "z":
            shift = ord(keyword[i % key_len]) - ord("a")
            result.append(chr((ord(char) - ord("a") - shift) % 26 + ord("a")))
        elif "A" <= char <= "Z":
            shift = ord(keyword[i % key_len].upper()) - ord("A")
            result.append(chr((ord(char) - ord("A") - shift) % 26 + ord("A")))
        else:
            result.append(char)

    return "".join(result)
