from typing import Any

import httpx

from agentevalops.config import SDKConfig
from agentevalops.exceptions import APIError, NetworkError
from agentevalops.tracer import TracerPlaceholder


class AgentEvalOps:
    """Primary client entrypoint for AgentEvalOps Python SDK."""

    def __init__(
        self,
        api_key: str | None = None,
        api_url: str | None = None,
        config: SDKConfig | None = None,
    ):
        if config:
            self.config = config
        else:
            self.config = SDKConfig(
                api_key=api_key or "",
                api_url=api_url or "http://localhost:8000",
            )

        self._headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "AgentEvalOps-Python-SDK/0.1.0",
        }
        self.tracer = TracerPlaceholder(client=self)

    def ping(self) -> dict[str, Any]:
        """Check API server availability."""
        try:
            with httpx.Client(timeout=self.config.timeout_seconds) as client:
                res = client.get(f"{self.config.api_url}/health", headers=self._headers)
                res.raise_for_status()
                data: dict[str, Any] = res.json()
                return data
        except httpx.HTTPStatusError as e:
            raise APIError(
                f"HTTP Error: {e.response.status_code}", status_code=e.response.status_code
            ) from e
        except httpx.RequestError as e:
            raise NetworkError(f"Failed to connect to AgentEvalOps API: {str(e)}") from e

    async def async_ping(self) -> dict[str, Any]:
        """Asynchronously check API server availability."""
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                res = await client.get(f"{self.config.api_url}/health", headers=self._headers)
                res.raise_for_status()
                data: dict[str, Any] = res.json()
                return data
        except httpx.HTTPStatusError as e:
            raise APIError(
                f"HTTP Error: {e.response.status_code}", status_code=e.response.status_code
            ) from e
        except httpx.RequestError as e:
            raise NetworkError(f"Failed to connect to AgentEvalOps API: {str(e)}") from e
