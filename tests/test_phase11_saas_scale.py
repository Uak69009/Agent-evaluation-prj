from fastapi.testclient import TestClient

from app.infrastructure.rate_limiter import RateLimiter
from app.infrastructure.security import security_manager
from app.main import app

client = TestClient(app)


def test_phase11_saas_security_and_rate_limiting():
    """Verify Phase 11 SaaS security, API Key hashing, PII scrubbing, and sliding window rate limiting."""
    # 1. API Key Generation & Hashing Verification
    gen = security_manager.generate_api_key(environment="live")
    assert gen.raw_key.startswith("aeo_live_")
    assert security_manager.verify_api_key(gen.raw_key, gen.key_hash) is True
    assert security_manager.verify_api_key("invalid_key", gen.key_hash) is False

    # 2. Secret Payload Scrubbing
    payload = {"query": "test", "authorization": "Bearer secret123", "password": "pass"}
    scrubbed = security_manager.scrub_sensitive_payload(payload)
    assert scrubbed["authorization"] == "[REDACTED_SECRET]"
    assert scrubbed["password"] == "[REDACTED_SECRET]"

    # 3. Sliding Window Rate Limiting Check
    limiter = RateLimiter(requests_per_minute=2)
    assert limiter.is_allowed("tenant_test") is True
    assert limiter.is_allowed("tenant_test") is True
    assert limiter.is_allowed("tenant_test") is False  # 3rd request in 60s blocked

    # 4. Test API Endpoint POST /api/v1/auth/api-keys
    res = client.post("/api/v1/auth/api-keys", json={"name": "Production Key", "environment": "live"})
    assert res.status_code == 201
    data = res.json()
    assert data["raw_key"].startswith("aeo_live_")
    assert len(data["key_hash"]) == 64
