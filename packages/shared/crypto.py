import hmac
import hashlib
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# In a real app, this should be a stable 32-byte key
AES_SECRET_KEY = os.getenv("AES_SECRET_KEY", b"12345678901234567890123456789012")

def encrypt_token(token: str) -> bytes:
    aesgcm = AESGCM(AES_SECRET_KEY if isinstance(AES_SECRET_KEY, bytes) else AES_SECRET_KEY.encode())
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, token.encode('utf-8'), None)
    return nonce + ciphertext

def decrypt_token(data: bytes) -> str:
    aesgcm = AESGCM(AES_SECRET_KEY if isinstance(AES_SECRET_KEY, bytes) else AES_SECRET_KEY.encode())
    nonce = data[:12]
    ciphertext = data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)
