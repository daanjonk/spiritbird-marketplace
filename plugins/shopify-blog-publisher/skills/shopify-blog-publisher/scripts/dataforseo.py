#!/usr/bin/env python3
"""DataForSEO API helper for keyword research.

Usage:
    python3 dataforseo.py suggestions "<seed_keyword>" [--location 2840] [--language en] [--limit 20]
    python3 dataforseo.py volume "<kw1>,<kw2>,<kw3>" [--location 2840] [--language en]
    python3 dataforseo.py related "<seed_keyword>" [--location 2840] [--language en] [--limit 10]

Required environment variables:
    DATAFORSEO_LOGIN       - Your DataForSEO login email
    DATAFORSEO_PASSWORD    - Your DataForSEO API password

  OR (alternative):
    DATAFORSEO_AUTH_TOKEN  - Pre-encoded Base64 token (login:password)
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

BASE_URL = "https://api.dataforseo.com/v3"


def get_auth_token():
    """Get the Base64 auth token from environment variables."""
    # Option 1: Pre-encoded token
    token = os.environ.get("DATAFORSEO_AUTH_TOKEN")
    if token:
        return token

    # Option 2: Login + password (will be base64-encoded)
    login = os.environ.get("DATAFORSEO_LOGIN")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if login and password:
        credentials = f"{login}:{password}"
        return base64.b64encode(credentials.encode()).decode()

    print(json.dumps({
        "error": "Missing DataForSEO credentials",
        "hint": "Set either DATAFORSEO_AUTH_TOKEN, or both DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD. See README.md for setup instructions."
    }, indent=2))
    sys.exit(1)


def api_request(endpoint: str, payload: list) -> dict:
    """Make a POST request to DataForSEO API."""
    auth_token = get_auth_token()
    url = f"{BASE_URL}/{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Basic {auth_token}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"error": f"HTTP {e.code}", "detail": body}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    if result.get("status_code") != 20000:
        print(json.dumps({"error": result.get("status_message", "Unknown error"), "raw": result}))
        sys.exit(1)

    return result


def cmd_suggestions(args):
    """Get keyword suggestions for a seed keyword."""
    payload = [{
        "keyword": args.keyword,
        "location_code": args.location,
        "language_code": args.language,
        "limit": args.limit,
        "include_seed_keyword": True,
        "order_by": ["keyword_info.search_volume,desc"]
    }]
    result = api_request("dataforseo_labs/google/keyword_suggestions/live", payload)

    items = []
    for task in result.get("tasks", []):
        for res in task.get("result", []):
            for item in res.get("items", []):
                kw_info = item.get("keyword_info", {})
                items.append({
                    "keyword": item.get("keyword"),
                    "search_volume": kw_info.get("search_volume"),
                    "competition": kw_info.get("competition_level"),
                    "competition_index": kw_info.get("competition"),
                    "cpc": kw_info.get("cpc"),
                })

    print(json.dumps({"keywords": items, "total_found": len(items), "cost": result.get("cost")}, indent=2))


def cmd_volume(args):
    """Get search volume for specific keywords."""
    keywords = [kw.strip() for kw in args.keywords.split(",") if kw.strip()]
    payload = [{
        "keywords": keywords,
        "location_code": args.location,
        "language_code": args.language,
    }]
    result = api_request("keywords_data/google_ads/search_volume/live", payload)

    items = []
    for task in result.get("tasks", []):
        for res in task.get("result", []):
            items.append({
                "keyword": res.get("keyword"),
                "search_volume": res.get("search_volume"),
                "competition": res.get("competition"),
                "competition_index": res.get("competition_index"),
                "cpc": res.get("cpc"),
                "low_bid": res.get("low_top_of_page_bid"),
                "high_bid": res.get("high_top_of_page_bid"),
                "monthly_searches": res.get("monthly_searches", [])[:6],
            })

    print(json.dumps({"keywords": items, "cost": result.get("cost")}, indent=2))


def cmd_related(args):
    """Get related keywords for a seed keyword."""
    payload = [{
        "keyword": args.keyword,
        "location_code": args.location,
        "language_code": args.language,
        "limit": args.limit,
        "order_by": ["keyword_data.keyword_info.search_volume,desc"]
    }]
    result = api_request("dataforseo_labs/google/related_keywords/live", payload)

    items = []
    for task in result.get("tasks", []):
        for res in task.get("result", []):
            for item in res.get("items", []):
                kw_data = item.get("keyword_data", {})
                kw_info = kw_data.get("keyword_info", {})
                items.append({
                    "keyword": kw_data.get("keyword"),
                    "search_volume": kw_info.get("search_volume"),
                    "competition": kw_info.get("competition_level"),
                    "competition_index": kw_info.get("competition"),
                    "cpc": kw_info.get("cpc"),
                })

    print(json.dumps({"keywords": items, "total_found": len(items), "cost": result.get("cost")}, indent=2))


def main():
    parser = argparse.ArgumentParser(description="DataForSEO keyword research tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Suggestions
    p_sug = subparsers.add_parser("suggestions", help="Get keyword suggestions")
    p_sug.add_argument("keyword", help="Seed keyword")
    p_sug.add_argument("--location", type=int, default=2840, help="Location code (default: 2840 = United States)")
    p_sug.add_argument("--language", default="en", help="Language code (default: en)")
    p_sug.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")

    # Volume
    p_vol = subparsers.add_parser("volume", help="Get search volume for keywords")
    p_vol.add_argument("keywords", help="Comma-separated keywords")
    p_vol.add_argument("--location", type=int, default=2840, help="Location code")
    p_vol.add_argument("--language", default="en", help="Language code")

    # Related
    p_rel = subparsers.add_parser("related", help="Get related keywords")
    p_rel.add_argument("keyword", help="Seed keyword")
    p_rel.add_argument("--location", type=int, default=2840, help="Location code")
    p_rel.add_argument("--language", default="en", help="Language code")
    p_rel.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")

    args = parser.parse_args()

    if args.command == "suggestions":
        cmd_suggestions(args)
    elif args.command == "volume":
        cmd_volume(args)
    elif args.command == "related":
        cmd_related(args)


if __name__ == "__main__":
    main()
