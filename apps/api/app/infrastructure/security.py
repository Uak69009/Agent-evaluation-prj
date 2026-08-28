import hashlib
import secrets
from typing import Any

from pydantic import BaseModel


class APIKeyGenerationResult(BaseModel):
    raw_key: str
    key_hash: str
    prefix: str


class SecurityManager:
    """Security management for multi-tenant API Key hashing and secret scrubbing."""

    @staticmethod
    def generate_api_key(environment: str = "test") -> APIKeyGenerationResult:
        prefix = f"aeo_{environment}_"
        secret = secrets.token_hex(16)
        raw_key = f"{prefix}{secret}"
        key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
        return APIKeyGenerationResult(
            raw_key=raw_key,
            key_hash=key_hash,
            prefix=prefix,
        )

    @staticmethod
    def verify_api_key(raw_key: str, expected_hash: str) -> bool:
        computed_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
        return secrets.compare_digest(computed_hash, expected_hash)

    @staticmethod
    def scrub_sensitive_payload(payload: dict[str, Any]) -> dict[str, Any]:
        scrubbed = payload.copy()
        for k in scrubbed.keys():
            if any(term in k.lower() for term in ["password", "secret", "token", "authorization"]):
                scrubbed[k] = "[REDACTED_SECRET]"
        return scrubbed


security_manager = SecurityManager()
