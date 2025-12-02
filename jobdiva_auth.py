"""Authentication helper for JobDiva API for S1NGULARITY.

Provides token-based authentication with optional Redis caching and automatic
refresh on expiration. Falls back to in-memory caching when Redis is not
configured.
"""

from __future__ import annotations

import os
import time
from typing import Optional

import requests

try:
    import redis  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    redis = None  # type: ignore


class JobDivaAuth:
    """Singleton authentication manager for JobDiva.

    The class keeps the access token cached and refreshes it automatically when
    expired. If Redis is available and `JOBDIVA_REDIS_URL` is set, the token and
    expiry are persisted across workers; otherwise, an in-memory cache is used.
    """

    _instance: Optional["JobDivaAuth"] = None
    _token_cache_key = "jobdiva:token"
    _token_expiry_key = "jobdiva:token_expiry"

    def __new__(cls) -> "JobDivaAuth":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.base_url = os.getenv("JOBDIVA_BASE_URL", "https://api.jobdiva.com")
        self.client_id = os.getenv("JOBDIVA_CLIENT_ID", "")
        self.username = os.getenv("JOBDIVA_USERNAME", "")
        self.password = os.getenv("JOBDIVA_PASSWORD", "")
        self.redis_client = self._init_redis()
        self._token: Optional[str] = None
        self._expiry: Optional[float] = None
        self._initialized = True

    def _init_redis(self):
        redis_url = os.getenv("JOBDIVA_REDIS_URL")
        if redis_url and redis:
            try:
                return redis.Redis.from_url(redis_url)
            except Exception:
                return None
        return None

    def _get_cached_token(self) -> tuple[Optional[str], Optional[float]]:
        if self.redis_client:
            try:
                token = self.redis_client.get(self._token_cache_key)
                expiry = self.redis_client.get(self._token_expiry_key)
                token_str = token.decode() if token else None
                expiry_val = float(expiry.decode()) if expiry else None
                return token_str, expiry_val
            except Exception:
                return None, None
        return self._token, self._expiry

    def _set_cached_token(self, token: str, expires_in: int) -> None:
        expiry_time = time.time() + max(expires_in - 30, 0)  # buffer
        if self.redis_client:
            try:
                ttl = int(expires_in)
                pipe = self.redis_client.pipeline()
                pipe.set(self._token_cache_key, token, ex=ttl)
                pipe.set(self._token_expiry_key, expiry_time, ex=ttl)
                pipe.execute()
            except Exception:
                self._token, self._expiry = token, expiry_time
                return
        self._token, self._expiry = token, expiry_time

    def authenticate(self) -> str:
        """Authenticate with JobDiva and cache the token."""

        auth_url = f"{self.base_url}/apiv2/authenticate"
        response = requests.get(
            auth_url,
            params={
                "clientid": self.client_id,
                "username": self.username,
                "password": self.password,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        token = data.get("access_token") or data.get("token")
        expires_in = int(data.get("expires_in", 3600))
        if not token:
            raise ValueError("Authentication response missing access_token")
        self._set_cached_token(token, expires_in)
        return token

    def get_token(self, force_refresh: bool = False) -> str:
        token, expiry = self._get_cached_token()
        if not force_refresh and token and expiry and time.time() < expiry:
            return token
        return self.authenticate()

    def authorized_headers(self) -> dict:
        token = self.get_token()
        return {"Authorization": f"Bearer {token}"}


def get_auth() -> JobDivaAuth:
    """Helper to obtain the singleton instance."""

    return JobDivaAuth()
