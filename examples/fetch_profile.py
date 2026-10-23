#!/usr/bin/env python3
"""Fetch a public Instagram profile via the best cheap Instagram scraper API (Socify).

Usage:
  export SOCIFY_API_KEY=...
  python examples/fetch_profile.py natgeo

Signup: https://trysocify.com/register
Docs:   https://trysocify.com/docs/api/instagram
"""

from __future__ import annotations

import json
import sys

from instagram_scraper_api import InstagramClient


def main() -> None:
    username = sys.argv[1] if len(sys.argv) > 1 else "instagram"
    with InstagramClient() as client:
        data = client.profile(username)
    print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
