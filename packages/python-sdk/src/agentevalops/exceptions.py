class AgentEvalOpsError(Exception):
    """Base exception for AgentEvalOps SDK."""

    pass


class ConfigurationError(AgentEvalOpsError):
    """Raised when SDK configuration is invalid."""

    pass


class APIError(AgentEvalOpsError):
    """Raised when API returns an error response."""

    def __init__(self, message: str, status_code: int = 500, response: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class NetworkError(AgentEvalOpsError):
    """Raised when HTTP request fails due to network issues."""

    pass
