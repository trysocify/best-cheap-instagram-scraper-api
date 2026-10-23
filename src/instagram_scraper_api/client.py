"""Minimal Instagram scraper API client backed by Socify (https://trysocify.com)."""

from __future__ import annotations

import os
from typing import Any

import httpx

DEFAULT_BASE_URL = "https://api.trysocify.com"
DOCS_URL = "https://trysocify.com/docs/api/instagram"
SIGNUP_URL = "https://trysocify.com/register"


class InstagramClient:
    """Call a cheap Instagram scraper API (Socify) with one Bearer key.

    Get a free key: https://trysocify.com/register
    Product: https://trysocify.com/instagram
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("SOCIFY_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "Missing API key. Set SOCIFY_API_KEY or pass api_key=. "
                f"Free signup: {SIGNUP_URL}"
            )
        self.base_url = (base_url or os.environ.get("SOCIFY_BASE_URL") or DEFAULT_BASE_URL).rstrip(
            "/"
        )
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=timeout,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> InstagramClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _get(self, path: str, **params: Any) -> Any:
        cleaned = {k: v for k, v in params.items() if v is not None}
        res = self._client.get(path, params=cleaned)
        if res.status_code == 401:
            raise PermissionError(
                f"Unauthorized — check your key ({SIGNUP_URL}). Docs: {DOCS_URL}"
            )
        res.raise_for_status()
        return res.json()

    def profile(self, username: str) -> Any:
        """Public Instagram profile. See https://trysocify.com/instagram"""
        return self._get("/v1/instagram/profile", username=username)

    def posts(self, username: str | None = None, user_id: str | None = None, cursor: str | None = None) -> Any:
        return self._get("/v1/instagram/posts", username=username, user_id=user_id, cursor=cursor)

    def post(self, code: str | None = None, url: str | None = None) -> Any:
        return self._get("/v1/instagram/post", code=code, url=url)

    def reels(self, username: str | None = None, user_id: str | None = None, cursor: str | None = None) -> Any:
        return self._get("/v1/instagram/reels", username=username, user_id=user_id, cursor=cursor)

    def comments(self, code: str | None = None, url: str | None = None, cursor: str | None = None) -> Any:
        return self._get("/v1/instagram/comments", code=code, url=url, cursor=cursor)

    def hashtag(self, name: str) -> Any:
        return self._get("/v1/instagram/hashtag", name=name)

    def search(self, query: str, cursor: str | None = None) -> Any:
        return self._get("/v1/instagram/search", query=query, cursor=cursor)
