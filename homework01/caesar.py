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
    for i in plaintext:
        suitable = 'A' <= i <= 'Z' or 'a' <= i <= 'z'
        if suitable:
            base_char_idx = ord('A' if 'A' <= i <= 'Z' else 'a')
            ciphertext += chr((ord(i) - base_char_idx + shift) % 26 + base_char_idx)
        else:
            ciphertext += i
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
    for i in ciphertext:
        suitable = 'A' <= i <= 'Z' or 'a' <= i <= 'z'
        if suitable:
            base_char_idx = ord('A' if 'A' <= i <= 'Z' else 'a')
            plaintext += chr((ord(i) - base_char_idx - shift) % 26 + base_char_idx)
        else:
            plaintext += i
    return plaintext