#!/usr/bin/env python3
"""List recent public Instagram posts — cheap Instagram scraper API example.

Signup: https://trysocify.com/register
Product: https://trysocify.com/instagram
"""

from __future__ import annotations

import json
import sys

from instagram_scraper_api import InstagramClient


def main() -> None:
    username = sys.argv[1] if len(sys.argv) > 1 else "natgeo"
    with InstagramClient() as client:
        data = client.posts(username=username)
    print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
