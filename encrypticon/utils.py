from cryptography.fernet import Fernet


def generate_key():
    """Generate a 32 byte key"""
    return Fernet.generate_key()


def encrypt_file(key: str, file_bytes: bytes) -> bytes:
    """Encrypt a file using the given key"""
    f = Fernet(key)
    return f.encrypt(file_bytes)


def decrypt_file(key: str, file_bytes: bytes) -> bytes:
    """Decrypt a file using the given key"""
    f = Fernet(key)
    return f.decrypt(file_bytes)
