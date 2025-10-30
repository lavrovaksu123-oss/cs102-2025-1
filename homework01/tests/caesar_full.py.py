import random
import string
import unittest


# Функции шифра Цезаря
def encrypt_caesar(plaintext, shift=0):
    result = []

    for char in plaintext:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            pos = ord(char) - base
            new_pos = (pos + shift) % 26
            new_char = chr(base + new_pos)
            result.append(new_char)
        else:
            result.append(char)
    return "".join(result)


def decrypt_caesar(ciphertext, shift=0):
    return encrypt_caesar(ciphertext, -shift)


# Юнит-тесты
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
                self.assertEqual(chiphertext, encrypt_caesar(plaintext, shift=shift))

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
                self.assertEqual(plaintext, decrypt_caesar(chiphertext, shift=shift))

    def test_randomized(self):
        shift = random.randint(8, 24)
        plaintext = "".join(
            random.choice(string.ascii_letters + " -,") for _ in range(64)
        )
        ciphertext = encrypt_caesar(plaintext, shift=shift)
        self.assertEqual(
            plaintext,
            decrypt_caesar(ciphertext, shift=shift),
            msg=f"shift={shift}, ciphertext={ciphertext}",
        )


if __name__ == "__main__":
    unittest.main()
