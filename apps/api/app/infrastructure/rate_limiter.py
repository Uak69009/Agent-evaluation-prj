import time


class RateLimiter:
    """Sliding-window tenant rate limiter for SaaS scale protection."""

    def __init__(self, requests_per_minute: int = 120):
        self.limit = requests_per_minute
        self._history: dict[str, list[float]] = {}

    def is_allowed(self, tenant_id: str) -> bool:
        now = time.time()
        window_start = now - 60.0

        if tenant_id not in self._history:
            self._history[tenant_id] = [now]
            return True

        # Keep timestamps within 60s window
        timestamps = [t for t in self._history[tenant_id] if t >= window_start]
        if len(timestamps) < self.limit:
            timestamps.append(now)
            self._history[tenant_id] = timestamps
            return True

        self._history[tenant_id] = timestamps
        return False


rate_limiter = RateLimiter(requests_per_minute=120)
