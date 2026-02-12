from cryptography.fernet import Fernet
from django.conf import settings


class EncryptionService:

    """
    EncryptionService handles symmetric encryption and decryption
    of sensitive patient information using Fernet.

    This service is responsible for:
    - Encrypting PHI (e.g., SSN, Passport)
    - Decrypting stored encrypted values
    - Ensuring encryption key is loaded from environment settings

    The encryption key must be configured in settings as FERNET_KEY.
    """

    def __init__(self):
        key = settings.FERNET_KEY
        if not key:
            raise ValueError("FERNET_KEY is not configured")
        self.fernet = Fernet(key)

    def encrypt(self, value: str) -> str:
        if not value:
            return None
        encrypted = self.fernet.encrypt(value.encode())
        return encrypted.decode()

    def decrypt(self, value: str) -> str:
        if not value:
            return None
        decrypted = self.fernet.decrypt(value.encode())
        return decrypted.decode()
