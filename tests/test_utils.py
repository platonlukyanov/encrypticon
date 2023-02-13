from encrypticon.utils import encrypt_file, decrypt_file, generate_key

mockFileBytes = b'Hello World'
key = generate_key()


def test_encrypt_file():
    encrypted = encrypt_file(key, mockFileBytes)
    assert encrypted != mockFileBytes


def test_decrypt_file():
    encrypted = encrypt_file(key, mockFileBytes)
    decrypted = decrypt_file(key, encrypted)
    assert decrypted == mockFileBytes
