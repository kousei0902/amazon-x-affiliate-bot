from datetime import datetime
from pathlib import Path

from .config import XConfig

DRAFTS_DIR = Path(__file__).resolve().parent.parent / "drafts"
IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def find_image(product_id: str) -> Path | None:
    """images/{product_id}.(jpg|jpeg|png|webp) があればそのパスを返す。
    SiteStripeで取得した商品画像をこの命名規則で保存しておくと自動で添付される。
    """
    for ext in IMAGE_EXTENSIONS:
        candidate = IMAGES_DIR / f"{product_id}{ext}"
        if candidate.exists():
            return candidate
    return None


def post_tweet(text: str, x_config: XConfig, product_id: str) -> str:
    """X APIキーが設定済みなら実際に投稿し、投稿IDを返す。
    未設定なら drafts/ にドラフトとして書き出し、実投稿はしない(dry-run)。
    images/{product_id}.jpg 等が存在すれば画像として添付する。
    """
    image_path = find_image(product_id)

    if x_config.is_configured:
        import tweepy

        media_ids = None
        if image_path:
            api = tweepy.API(
                tweepy.OAuth1UserHandler(
                    x_config.api_key,
                    x_config.api_secret,
                    x_config.access_token,
                    x_config.access_secret,
                )
            )
            media = api.media_upload(filename=str(image_path))
            media_ids = [media.media_id]

        client = tweepy.Client(
            consumer_key=x_config.api_key,
            consumer_secret=x_config.api_secret,
            access_token=x_config.access_token,
            access_token_secret=x_config.access_secret,
        )
        response = client.create_tweet(text=text, media_ids=media_ids)
        return str(response.data["id"])

    return _write_draft(text, product_id, image_path)


def _write_draft(text: str, product_id: str, image_path: Path | None) -> str:
    DRAFTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    draft_path = DRAFTS_DIR / f"{timestamp}_{product_id}.txt"
    note = f"\n\n[添付画像: {image_path}]" if image_path else "\n\n[添付画像: なし(images/フォルダに画像がありません)]"
    draft_path.write_text(text + note, encoding="utf-8")
    return f"DRAFT:{draft_path.name}"
