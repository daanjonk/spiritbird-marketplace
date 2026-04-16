#!/usr/bin/env python3
"""Shopify Blog API helper for authentication and article publishing.

Usage:
    python3 shopify.py auth
    python3 shopify.py publish --token <token> --title <title> --body <html> [--tags <tags>] [--image-url <url>] [--published true|false]
    python3 shopify.py list-articles --token <token> [--limit 5]

Required environment variables:
    SHOPIFY_STORE          - Your Shopify store domain (e.g., your-store.myshopify.com)
    SHOPIFY_BLOG_ID        - The blog ID to publish articles to
    SHOPIFY_CLIENT_ID      - Shopify app client ID
    SHOPIFY_CLIENT_SECRET  - Shopify app client secret

Optional environment variables:
    SHOPIFY_API_VERSION    - API version (default: 2025-01)
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse


def get_config():
    """Load configuration from environment variables."""
    required = {
        "SHOPIFY_STORE": os.environ.get("SHOPIFY_STORE"),
        "SHOPIFY_BLOG_ID": os.environ.get("SHOPIFY_BLOG_ID"),
        "SHOPIFY_CLIENT_ID": os.environ.get("SHOPIFY_CLIENT_ID"),
        "SHOPIFY_CLIENT_SECRET": os.environ.get("SHOPIFY_CLIENT_SECRET"),
    }

    missing = [k for k, v in required.items() if not v]
    if missing:
        print(json.dumps({
            "error": "Missing required environment variables",
            "missing": missing,
            "hint": "Set these in your .env file or export them in your shell. See README.md for setup instructions."
        }, indent=2))
        sys.exit(1)

    return {
        "store": required["SHOPIFY_STORE"],
        "blog_id": required["SHOPIFY_BLOG_ID"],
        "client_id": required["SHOPIFY_CLIENT_ID"],
        "client_secret": required["SHOPIFY_CLIENT_SECRET"],
        "api_version": os.environ.get("SHOPIFY_API_VERSION", "2025-01"),
    }


def shopify_request(config: dict, method: str, endpoint: str, token: str = None, data: dict = None) -> dict:
    """Make a request to the Shopify Admin API."""
    url = f"https://{config['store']}/admin/api/{config['api_version']}/{endpoint}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("X-Shopify-Access-Token", token)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"error": f"HTTP {e.code}", "detail": detail}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def cmd_auth(args):
    """Exchange client credentials for an access token."""
    config = get_config()
    url = f"https://{config['store']}/admin/oauth/access_token"
    params = urllib.parse.urlencode({
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "grant_type": "client_credentials",
    }).encode("utf-8")

    req = urllib.request.Request(url, data=params, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"error": f"HTTP {e.code}", "detail": detail}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    print(json.dumps({
        "access_token": result.get("access_token"),
        "scope": result.get("scope"),
        "expires_in": result.get("expires_in"),
    }, indent=2))


def cmd_publish(args):
    """Create a blog article."""
    config = get_config()
    article = {
        "title": args.title,
        "body_html": args.body,
    }

    if args.tags:
        article["tags"] = args.tags
    if args.image_url:
        article["image"] = {"src": args.image_url}
    if args.published:
        if args.published.lower() == "false":
            article["published"] = False
        else:
            article["published"] = True

    result = shopify_request(config, "POST", f"blogs/{config['blog_id']}/articles.json", token=args.token, data={"article": article})

    art = result.get("article", {})
    output = {
        "id": art.get("id"),
        "title": art.get("title"),
        "handle": art.get("handle"),
        "published_at": art.get("published_at"),
        "url": f"https://{config['store']}/blogs/news/{art.get('handle', '')}",
        "admin_url": f"https://{config['store']}/admin/articles/{art.get('id', '')}",
        "tags": art.get("tags"),
    }
    print(json.dumps(output, indent=2))


def cmd_list_articles(args):
    """List recent blog articles."""
    config = get_config()
    limit = args.limit or 5
    result = shopify_request(config, "GET", f"blogs/{config['blog_id']}/articles.json?limit={limit}", token=args.token)

    articles = []
    for art in result.get("articles", []):
        articles.append({
            "id": art.get("id"),
            "title": art.get("title"),
            "handle": art.get("handle"),
            "published_at": art.get("published_at"),
            "tags": art.get("tags"),
        })
    print(json.dumps({"articles": articles}, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Shopify Blog API tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Auth
    subparsers.add_parser("auth", help="Get access token via client credentials")

    # Publish
    p_pub = subparsers.add_parser("publish", help="Create a blog article")
    p_pub.add_argument("--token", required=True, help="Shopify access token")
    p_pub.add_argument("--title", required=True, help="Article title")
    p_pub.add_argument("--body", required=True, help="Article body (HTML)")
    p_pub.add_argument("--tags", help="Comma-separated tags")
    p_pub.add_argument("--image-url", help="Featured image URL")
    p_pub.add_argument("--published", default="true", help="Publish immediately (true/false)")

    # List
    p_list = subparsers.add_parser("list-articles", help="List recent articles")
    p_list.add_argument("--token", required=True, help="Shopify access token")
    p_list.add_argument("--limit", type=int, default=5, help="Number of articles")

    args = parser.parse_args()

    if args.command == "auth":
        cmd_auth(args)
    elif args.command == "publish":
        cmd_publish(args)
    elif args.command == "list-articles":
        cmd_list_articles(args)


if __name__ == "__main__":
    main()
