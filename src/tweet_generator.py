from .models import Product

MAX_WEIGHTED_LENGTH = 280
URL_WEIGHTED_LENGTH = 23  # Xはどんな長さのURLもt.coで23文字換算
DISCLOSURE = "【PR】"  # 景品表示法のステマ規制対応。ステルスマーケティングを避けるため必須


def weighted_length(text: str) -> int:
    """X(旧Twitter)の文字数カウント方式を簡易再現。全角相当は2文字換算。"""
    length = 0
    for ch in text:
        length += 2 if ord(ch) > 0x2E80 else 1
    return length


def truncate_to_weighted(text: str, max_len: int) -> str:
    result = ""
    total = 0
    for ch in text:
        w = 2 if ord(ch) > 0x2E80 else 1
        if total + w > max_len:
            break
        result += ch
        total += w
    return result


def build_tweet(product: Product) -> str:
    """共感を呼ぶ一言(hook)→商品名→ハッシュタグ→リンク の順で組み立てる。
    hookが空の場合は従来通り商品名のみの構成にフォールバックする。
    """
    hashtags = " ".join(f"#{t}" for t in product.tags)
    price_part = f" {product.price}円" if product.price else ""

    if product.hook:
        # 名前以外の固定部分(装飾+hook行+価格+ハッシュタグ行+URL行+改行)の文字数を先に見積もる
        non_name_text = (
            DISCLOSURE + product.hook + "\n" + price_part + ("\n" + hashtags if hashtags else "") + "\n"
        )
        fixed_weighted = weighted_length(non_name_text) + URL_WEIGHTED_LENGTH
        budget_for_name = MAX_WEIGHTED_LENGTH - fixed_weighted
        name = truncate_to_weighted(product.name, max(budget_for_name, 0))

        lines = [f"{DISCLOSURE}{product.hook}", f"{name}{price_part}"]
    else:
        non_name_text = DISCLOSURE + price_part + ("\n" + hashtags if hashtags else "") + "\n"
        fixed_weighted = weighted_length(non_name_text) + URL_WEIGHTED_LENGTH
        budget_for_name = MAX_WEIGHTED_LENGTH - fixed_weighted
        name = truncate_to_weighted(product.name, max(budget_for_name, 0))

        lines = [f"{DISCLOSURE}{name}{price_part}"]

    if hashtags:
        lines.append(hashtags)
    lines.append(product.affiliate_url)
    return "\n".join(lines)
