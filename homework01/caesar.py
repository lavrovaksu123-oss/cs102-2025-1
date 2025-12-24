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
        if 'A' <= i <= 'Z':
            i_new = chr((ord(i) - ord('A') + shift) % 26 + ord('A'))
            ciphertext += i_new
        elif 'a' <= i <= 'z':
            i_new = chr((ord(i) - ord('a') + shift) % 26 + ord('a'))
            ciphertext += i_new
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
        if 'A' <= i <= 'Z':
            i_new = chr((ord(i) - ord('A') - shift) % 26 + ord('A'))
            plaintext += i_new
        elif 'a' <= i <= 'z':
            i_new = chr((ord(i) - ord('a') - shift) % 26 + ord('a'))
            plaintext += i_new
        else:
            plaintext += i
    return plaintext