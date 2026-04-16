"""
Configuration for AI Product Images skill.

╔══════════════════════════════════════════════════════════════════╗
║  SETUP: Fill in your credentials below before using this skill  ║
╚══════════════════════════════════════════════════════════════════╝

Instructions:
1. SHOPIFY: Get your store domain, client ID, and client secret
   from your Shopify custom app (Settings → Apps → Develop apps).
   The app needs these scopes: read_products, write_products, write_files.

2. CLOUDINARY: Your cloud name is in the Cloudinary dashboard.
   The folder name is where you store product reference images.
   Cloudinary is connected via the Cloudinary MCP connector — no
   API key needed here, but you DO need the connector installed.

3. MODEL REFERENCES: Upload 2-3 photos of your model to Shopify
   Files (Settings → Files) and paste the permanent CDN URLs below.
   These give character consistency across all generated images.
   Leave empty if you don't use model-on-product shots.
"""

# ─────────────────────────────────────────────────────────────────
# SHOPIFY STORE
# ─────────────────────────────────────────────────────────────────
STORE = "YOUR-STORE.myshopify.com"           # e.g. "my-brand.myshopify.com"
API_VERSION = "2025-01"                      # Shopify API version

# Shopify Custom App credentials (client credentials grant flow)
CLIENT_ID = "YOUR_SHOPIFY_CLIENT_ID"         # e.g. "28b9b390..."  (32-char hex string)
CLIENT_SECRET = "YOUR_SHOPIFY_CLIENT_SECRET" # e.g. "shpss_bb8c..." (starts with "shpss_")

# ─────────────────────────────────────────────────────────────────
# CLOUDINARY (for product reference images)
# ─────────────────────────────────────────────────────────────────
CLOUDINARY_CLOUD_NAME = "YOUR_CLOUD_NAME"    # e.g. "dxyz123ab"
CLOUDINARY_PRODUCT_FOLDER = "Shopify product images"  # default folder name — change if you use a different one

# ─────────────────────────────────────────────────────────────────
# MODEL REFERENCE IMAGES (for character consistency)
# ─────────────────────────────────────────────────────────────────
# Upload model photos to Shopify Files and paste the CDN URLs here.
# Use 2-3 images showing the model from different angles.
# Leave as empty list if you don't use model+product shots.
MODEL_REFS = [
    # "https://cdn.shopify.com/s/files/1/XXXX/XXXX/XXXX/files/model_front.png?v=...",
    # "https://cdn.shopify.com/s/files/1/XXXX/XXXX/XXXX/files/model_side.png?v=...",
]
