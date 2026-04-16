#!/usr/bin/env python3
"""Shopify Products API helper for listing products and managing product images.

Usage:
    python3 shopify_products.py auth
    python3 shopify_products.py list-products --token <token> [--limit 10] [--title "search term"] [--collection-id <id>]
    python3 shopify_products.py get-product --token <token> --product-id <id>
    python3 shopify_products.py list-collections --token <token> [--limit 10]
    python3 shopify_products.py add-image --token <token> --product-id <id> --image-url <url> [--alt "alt text"] [--position 1]
    python3 shopify_products.py list-images --token <token> --product-id <id>
    python3 shopify_products.py delete-image --token <token> --product-id <id> --image-id <image_id>
    python3 shopify_products.py upload-file --token <token> --url <url> [--alt "description"]
    python3 shopify_products.py list-files --token <token> [--limit 10]

Configuration:
    All credentials are in config.py (same directory). Fill those in before first use.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

# Import configuration from config.py (same directory as this script)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import STORE, API_VERSION, CLIENT_ID, CLIENT_SECRET


def shopify_request(method: str, endpoint: str, token: str = None, data: dict = None) -> dict:
    """Make a request to the Shopify Admin API."""
    url = f"https://{STORE}/admin/api/{API_VERSION}/{endpoint}"
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
    url = f"https://{STORE}/admin/oauth/access_token"
    params = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
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


def cmd_list_products(args):
    """List products, optionally filtered by title or collection."""
    limit = args.limit or 10

    if args.collection_id:
        endpoint = f"collections/{args.collection_id}/products.json?limit={limit}"
    else:
        endpoint = f"products.json?limit={limit}&status=active"

    if args.title:
        endpoint += f"&title={urllib.parse.quote(args.title)}"

    result = shopify_request("GET", endpoint, token=args.token)

    products = []
    for p in result.get("products", []):
        images = p.get("images", [])
        products.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "handle": p.get("handle"),
            "status": p.get("status"),
            "product_type": p.get("product_type"),
            "vendor": p.get("vendor"),
            "body_html_preview": (p.get("body_html") or "")[:200],
            "image_count": len(images),
            "has_images": len(images) > 0,
            "first_image_url": images[0].get("src") if images else None,
            "tags": p.get("tags"),
            "variants_count": len(p.get("variants", [])),
            "url": f"https://{STORE}/products/{p.get('handle', '')}",
            "admin_url": f"https://{STORE}/admin/products/{p.get('id', '')}",
        })
    print(json.dumps({"products": products, "count": len(products)}, indent=2))


def cmd_get_product(args):
    """Get a single product with full details."""
    result = shopify_request("GET", f"products/{args.product_id}.json", token=args.token)

    p = result.get("product", {})
    images = p.get("images", [])
    variants = p.get("variants", [])

    output = {
        "id": p.get("id"),
        "title": p.get("title"),
        "handle": p.get("handle"),
        "body_html": p.get("body_html"),
        "product_type": p.get("product_type"),
        "vendor": p.get("vendor"),
        "status": p.get("status"),
        "tags": p.get("tags"),
        "images": [{"id": img.get("id"), "src": img.get("src"), "alt": img.get("alt"), "position": img.get("position")} for img in images],
        "variants": [{"id": v.get("id"), "title": v.get("title"), "price": v.get("price"), "sku": v.get("sku")} for v in variants],
        "url": f"https://{STORE}/products/{p.get('handle', '')}",
        "admin_url": f"https://{STORE}/admin/products/{p.get('id', '')}",
    }
    print(json.dumps(output, indent=2))


def cmd_list_collections(args):
    """List collections (both custom and smart)."""
    limit = args.limit or 10

    # Get custom collections
    custom = shopify_request("GET", f"custom_collections.json?limit={limit}", token=args.token)
    # Get smart collections
    smart = shopify_request("GET", f"smart_collections.json?limit={limit}", token=args.token)

    collections = []
    for c in custom.get("custom_collections", []):
        collections.append({
            "id": c.get("id"),
            "title": c.get("title"),
            "handle": c.get("handle"),
            "type": "custom",
            "products_count": c.get("products_count"),
        })
    for c in smart.get("smart_collections", []):
        collections.append({
            "id": c.get("id"),
            "title": c.get("title"),
            "handle": c.get("handle"),
            "type": "smart",
            "products_count": c.get("products_count"),
        })

    print(json.dumps({"collections": collections, "count": len(collections)}, indent=2))


def cmd_add_image(args):
    """Add an image to a product from a URL."""
    image_data = {
        "src": args.image_url,
    }
    if args.alt:
        image_data["alt"] = args.alt
    if args.position:
        image_data["position"] = args.position

    result = shopify_request(
        "POST",
        f"products/{args.product_id}/images.json",
        token=args.token,
        data={"image": image_data}
    )

    img = result.get("image", {})
    output = {
        "id": img.get("id"),
        "product_id": img.get("product_id"),
        "src": img.get("src"),
        "alt": img.get("alt"),
        "position": img.get("position"),
        "width": img.get("width"),
        "height": img.get("height"),
        "admin_url": f"https://{STORE}/admin/products/{args.product_id}",
    }
    print(json.dumps(output, indent=2))


def cmd_list_images(args):
    """List all images for a product."""
    result = shopify_request("GET", f"products/{args.product_id}/images.json", token=args.token)

    images = []
    for img in result.get("images", []):
        images.append({
            "id": img.get("id"),
            "src": img.get("src"),
            "alt": img.get("alt"),
            "position": img.get("position"),
            "width": img.get("width"),
            "height": img.get("height"),
        })
    print(json.dumps({"images": images, "count": len(images)}, indent=2))


def cmd_delete_image(args):
    """Delete a specific image from a product."""
    shopify_request(
        "DELETE",
        f"products/{args.product_id}/images/{args.image_id}.json",
        token=args.token
    )
    print(json.dumps({"deleted": True, "image_id": args.image_id, "product_id": args.product_id}))


def graphql_request(query: str, variables: dict = None, token: str = None) -> dict:
    """Make a GraphQL request to the Shopify Admin API."""
    url = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
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


def cmd_upload_file(args):
    """Upload an image to Shopify Files (permanent CDN hosting)."""
    import time

    query = '''
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files {
          ... on MediaImage {
            id
            alt
            image {
              url
            }
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    '''
    variables = {
        "files": [{
            "alt": args.alt or "",
            "contentType": "IMAGE",
            "originalSource": args.url,
        }]
    }

    result = graphql_request(query, variables, token=args.token)
    data = result.get("data", {}).get("fileCreate", {})

    errors = data.get("userErrors", [])
    if errors:
        print(json.dumps({"error": "Upload failed", "details": errors}))
        sys.exit(1)

    files = data.get("files", [])
    if not files:
        print(json.dumps({"error": "No file returned"}))
        sys.exit(1)

    file_id = files[0].get("id")

    # Poll for the image URL to become available (Shopify processes async)
    get_query = '''
    query($id: ID!) {
      node(id: $id) {
        ... on MediaImage {
          id
          alt
          status
          image {
            url
            width
            height
          }
        }
      }
    }
    '''

    for _ in range(10):
        time.sleep(2)
        check = graphql_request(get_query, {"id": file_id}, token=args.token)
        node = check.get("data", {}).get("node", {})
        if node.get("image") and node["image"].get("url"):
            print(json.dumps({
                "id": node.get("id"),
                "alt": node.get("alt"),
                "status": node.get("status"),
                "url": node["image"]["url"],
                "width": node["image"].get("width"),
                "height": node["image"].get("height"),
            }, indent=2))
            return

    # If we get here, the image isn't ready yet
    print(json.dumps({"id": file_id, "status": "processing", "message": "Image uploaded but still processing. Check Shopify Files in a moment."}))


def cmd_list_files(args):
    """List recent files from Shopify Files."""
    limit = args.limit or 10
    query = '''
    query($first: Int!) {
      files(first: $first, sortKey: CREATED_AT, reverse: true) {
        edges {
          node {
            ... on MediaImage {
              id
              alt
              createdAt
              image {
                url
                width
                height
              }
            }
          }
        }
      }
    }
    '''

    result = graphql_request(query, {"first": limit}, token=args.token)
    edges = result.get("data", {}).get("files", {}).get("edges", [])

    files = []
    for edge in edges:
        node = edge.get("node", {})
        if node.get("image"):
            files.append({
                "id": node.get("id"),
                "alt": node.get("alt"),
                "url": node["image"].get("url"),
                "width": node["image"].get("width"),
                "height": node["image"].get("height"),
                "created_at": node.get("createdAt"),
            })
    print(json.dumps({"files": files, "count": len(files)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Shopify Products API tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Auth
    subparsers.add_parser("auth", help="Get access token via client credentials")

    # List products
    p_list = subparsers.add_parser("list-products", help="List products")
    p_list.add_argument("--token", required=True, help="Shopify access token")
    p_list.add_argument("--limit", type=int, default=10, help="Number of products")
    p_list.add_argument("--title", help="Filter by title (partial match)")
    p_list.add_argument("--collection-id", help="Filter by collection ID")

    # Get product
    p_get = subparsers.add_parser("get-product", help="Get a single product")
    p_get.add_argument("--token", required=True, help="Shopify access token")
    p_get.add_argument("--product-id", required=True, help="Product ID")

    # List collections
    p_coll = subparsers.add_parser("list-collections", help="List collections")
    p_coll.add_argument("--token", required=True, help="Shopify access token")
    p_coll.add_argument("--limit", type=int, default=10, help="Number per type")

    # Add image
    p_add = subparsers.add_parser("add-image", help="Add image to product")
    p_add.add_argument("--token", required=True, help="Shopify access token")
    p_add.add_argument("--product-id", required=True, help="Product ID")
    p_add.add_argument("--image-url", required=True, help="Image URL to upload")
    p_add.add_argument("--alt", help="Image alt text")
    p_add.add_argument("--position", type=int, help="Image position (1 = first)")

    # List images
    p_imgs = subparsers.add_parser("list-images", help="List product images")
    p_imgs.add_argument("--token", required=True, help="Shopify access token")
    p_imgs.add_argument("--product-id", required=True, help="Product ID")

    # Delete image
    p_del = subparsers.add_parser("delete-image", help="Delete a product image")
    p_del.add_argument("--token", required=True, help="Shopify access token")
    p_del.add_argument("--product-id", required=True, help="Product ID")
    p_del.add_argument("--image-id", required=True, help="Image ID to delete")

    # Upload file to Shopify Files (permanent CDN hosting)
    p_upload = subparsers.add_parser("upload-file", help="Upload image to Shopify Files for permanent hosting")
    p_upload.add_argument("--token", required=True, help="Shopify access token")
    p_upload.add_argument("--url", required=True, help="Public image URL to upload")
    p_upload.add_argument("--alt", help="Image alt text / description")

    # List files from Shopify Files
    p_files = subparsers.add_parser("list-files", help="List recent files from Shopify Files")
    p_files.add_argument("--token", required=True, help="Shopify access token")
    p_files.add_argument("--limit", type=int, default=10, help="Number of files")

    args = parser.parse_args()

    commands = {
        "auth": cmd_auth,
        "list-products": cmd_list_products,
        "get-product": cmd_get_product,
        "list-collections": cmd_list_collections,
        "add-image": cmd_add_image,
        "list-images": cmd_list_images,
        "delete-image": cmd_delete_image,
        "upload-file": cmd_upload_file,
        "list-files": cmd_list_files,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
