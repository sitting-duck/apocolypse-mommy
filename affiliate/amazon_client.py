# amazon_client.py — minimal affiliate search using python-amazon-paapi
import os
from typing import List, Dict
from amazon_paapi import AmazonApi

ACCESS  = os.environ["PAAPI_ACCESS_KEY"]
SECRET  = os.environ["PAAPI_SECRET_KEY"]
TAG     = os.environ["PAAPI_PARTNER_TAG"]   # e.g., apocalypseprep-20
COUNTRY = "US"                              # 'US','CA','UK','DE', etc.

amazon = AmazonApi(ACCESS, SECRET, TAG, COUNTRY)

def search_affiliate_links(keywords: str, n: int = 5) -> List[Dict]:
    res = amazon.search_items(keywords=keywords)
    items = getattr(res, "items", [])[:n]
    out = []
    for it in items:
        title = it.item_info.title.display_value if it.item_info and it.item_info.title else None
        url   = it.detail_page_url                       # includes your affiliate tag
        price = None
        if it.offers and it.offers.listings:
            p = it.offers.listings[0].price
            if p and p.display_amount:
                price = p.display_amount
        out.append({"asin": it.asin, "title": title, "url": url, "price": price})
    return out

