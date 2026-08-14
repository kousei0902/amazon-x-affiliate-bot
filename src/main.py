from pathlib import Path

from .config import load_config
from .product_source import load_pending, mark_posted
from .tweet_generator import build_tweet
from .x_client import post_tweet

PRODUCTS_CSV = Path(__file__).resolve().parent.parent / "products.csv"


def run() -> None:
    config = load_config()
    pending = load_pending(PRODUCTS_CSV)

    if not pending:
        print("投稿待ちの商品がありません。products.csv に追加してください。")
        return

    if not config.x.is_configured:
        print("[dry-run] X APIキー未設定のため drafts/ にツイート案を保存します。\n")

    targets = pending[: config.posts_per_run]
    for product in targets:
        tweet_text = build_tweet(product)
        result = post_tweet(tweet_text, config.x, product.id)
        mark_posted(PRODUCTS_CSV, product.id)
        print(f"[{product.id}] -> {result}")
        print(tweet_text)
        print("-" * 40)


if __name__ == "__main__":
    run()
