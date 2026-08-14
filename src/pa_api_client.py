"""PA-API (Product Advertising API) 連携。

Amazon アソシエイトの実績要件(180日以内に3件以上の紹介実績)を満たして
API キーが発行されるまでは未使用。.env にキーを設定すると
fetch_products() が有効になり、ASIN から商品名・価格・画像・最新の
アフィリエイトリンクを自動取得できるようになる。
"""

from .config import AmazonConfig
from .models import Product


class PaApiNotConfigured(RuntimeError):
    pass


def fetch_products(asins: list[str], amazon_config: AmazonConfig) -> list[Product]:
    if not amazon_config.is_configured:
        raise PaApiNotConfigured(
            "AMAZON_ACCESS_KEY / AMAZON_SECRET_KEY / AMAZON_ASSOCIATE_TAG が "
            ".env に未設定です。PA-API キー取得後に設定してください。"
        )

    # amazon-paapi (pip) を使った実装。キー取得後に有効化される。
    from amazon_paapi import AmazonApi

    api = AmazonApi(
        amazon_config.access_key,
        amazon_config.secret_key,
        amazon_config.associate_tag,
        amazon_config.country,
    )
    items = api.get_items(asins)

    products = []
    for item in items:
        price = ""
        if item.offers and item.offers.listings:
            price = str(item.offers.listings[0].price.amount)
        products.append(
            Product(
                id=item.asin,
                asin=item.asin,
                name=item.item_info.title.display_value if item.item_info and item.item_info.title else "",
                price=price,
                affiliate_url=item.detail_page_url,
            )
        )
    return products
