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
import random
import string
import unittest

import caesar


class CaesarTestCase(unittest.TestCase):
    def test_encrypt(self):
        cases = [
            ("", 0, ""),
            ("python", 0, "python"),
            ("PYTHON", 0, "PYTHON"),
            ("Python", 0, "Python"),
            ("Python3.6", 0, "Python3.6"),
            ("", 3, ""),
            ("PYTHON", 3, "SBWKRQ"),
            ("python", 3, "sbwkrq"),
            ("Python", 3, "Sbwkrq"),
            ("Python3.6", 3, "Sbwkrq3.6"),
        ]

        for i, (plaintext, shift, chiphertext) in enumerate(cases):
            with self.subTest(case=i, plaintext=plaintext, chiphertext=chiphertext):
                self.assertEqual(chiphertext, caesar.encrypt_caesar(plaintext, shift=shift))

    def test_decrypt(self):
        cases = [
            ("", 0, ""),
            ("python", 0, "python"),
            ("PYTHON", 0, "PYTHON"),
            ("Python", 0, "Python"),
            ("Python3.6", 0, "Python3.6"),
            ("", 3, ""),
            ("SBWKRQ", 3, "PYTHON"),
            ("sbwkrq", 3, "python"),
            ("Sbwkrq", 3, "Python"),
            ("Sbwkrq3.6", 3, "Python3.6"),
        ]

        for i, (chiphertext, shift, plaintext) in enumerate(cases):
            with self.subTest(case=i, chiphertext=chiphertext, plaintext=plaintext):
                self.assertEqual(plaintext, caesar.decrypt_caesar(chiphertext, shift=shift))

    def test_randomized(self):
        shift = random.randint(8, 24)
        plaintext = "".join(random.choice(string.ascii_letters + " -,") for _ in range(64))
        ciphertext = caesar.encrypt_caesar(plaintext, shift=shift)
        self.assertEqual(
            plaintext,
            caesar.decrypt_caesar(ciphertext, shift=shift),
            msg=f"shift={shift}, ciphertext={ciphertext}",
        )
