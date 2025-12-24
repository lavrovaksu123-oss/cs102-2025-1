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
    idx = 0
    ciphertext = ""
    for i in plaintext:
        suitable = 'A' <= i <= 'Z' or 'a' <= i <= 'z'
        if suitable:
            base_char_idx = ord('A' if 'A' <= i <= 'Z' else 'a')
            if idx >= len(keyword):
                idx = 0
            shift = ord(keyword[idx]) - base_char_idx
            ciphertext += chr((ord(i) - base_char_idx + shift) % 26 + base_char_idx)
            idx += 1
        else:
            ciphertext += i
    return ciphertext


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

    idx = 0
    plaintext = ""
    for i in ciphertext:
        suitable = 'A' <= i <= 'Z' or 'a' <= i <= 'z'
        if suitable:
            base_char_idx = ord('A' if 'A' <= i <= 'Z' else 'a')
            if idx >= len(keyword):
                idx = 0
            shift = ord(keyword[idx]) - base_char_idx
            plaintext += chr((ord(i) - base_char_idx - shift) % 26 + base_char_idx)
            idx += 1
        else:
            plaintext += i
    return plaintext