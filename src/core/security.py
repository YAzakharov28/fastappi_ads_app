import hashlib
import secrets

import bcrypt


def _password_digest(password: str) -> bytes:
    """SHA-256 прехэш для устранения ограничения длины пароля в bcrypt."""
    return hashlib.sha256(password.encode("utf-8")).digest()


def hash_password(password: str) -> str:
    """Хэширует пароль через bcrypt с предварительным SHA-256 прехэшем."""
    digest = _password_digest(password)
    return bcrypt.hashpw(digest, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Проверяет пароль, сравнивая его хэш с сохранённым bcrypt-хэшем."""
    digest = _password_digest(password)
    return bcrypt.checkpw(digest, password_hash.encode("utf-8"))


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    return token, hash_token(token)