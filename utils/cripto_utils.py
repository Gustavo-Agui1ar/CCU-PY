import os
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "../configs")
KEY_PATH = os.path.join(CONFIG_DIR, "secret.key")


class CriptoUtils:
    _fernet: Fernet | None = None

    @staticmethod
    def _load_fernet() -> Fernet:
        if CriptoUtils._fernet is not None:
            return CriptoUtils._fernet

        os.makedirs(CONFIG_DIR, exist_ok=True)

        if not os.path.exists(KEY_PATH):
            key = Fernet.generate_key()
            with open(KEY_PATH, "wb") as f:
                f.write(key)
        else:
            with open(KEY_PATH, "rb") as f:
                key = f.read()

        CriptoUtils._fernet = Fernet(key)
        return CriptoUtils._fernet

    @staticmethod
    def encrypt(value: str) -> str:
        if not value:
            return ""
        fernet = CriptoUtils._load_fernet()
        return fernet.encrypt(value.encode()).decode()

    @staticmethod
    def decrypt(value: str) -> str:
        if not value:
            return ""
        try:
            fernet = CriptoUtils._load_fernet()
            return fernet.decrypt(value.encode()).decode()
        except Exception:
            return ""
