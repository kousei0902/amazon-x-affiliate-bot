from datetime import datetime
from pathlib import Path

from .config import XConfig

DRAFTS_DIR = Path(__file__).resolve().parent.parent / "drafts"


def post_tweet(text: str, x_config: XConfig, product_id: str) -> str:
    """X APIキーが設定済みなら実際に投稿し、投稿IDを返す。
    未設定なら drafts/ にドラフトとして書き出し、実投稿はしない(dry-run)。
    """
    if x_config.is_configured:
        import tweepy

        client = tweepy.Client(
            consumer_key=x_config.api_key,
            consumer_secret=x_config.api_secret,
            access_token=x_config.access_token,
            access_token_secret=x_config.access_secret,
        )
        response = client.create_tweet(text=text)
        return str(response.data["id"])

    return _write_draft(text, product_id)


def _write_draft(text: str, product_id: str) -> str:
    DRAFTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    draft_path = DRAFTS_DIR / f"{timestamp}_{product_id}.txt"
    draft_path.write_text(text, encoding="utf-8")
    return f"DRAFT:{draft_path.name}"
