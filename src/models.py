from dataclasses import dataclass, field


@dataclass
class Product:
    id: str
    name: str
    price: str
    affiliate_url: str
    asin: str = ""
    tags: list[str] = field(default_factory=list)
    posted: bool = False
    hook: str = ""

    @staticmethod
    def from_row(row: dict) -> "Product":
        tags_raw = (row.get("tags") or "").strip()
        tags = [t.strip() for t in tags_raw.split("|") if t.strip()] if tags_raw else []
        return Product(
            id=row["id"],
            name=row["name"],
            price=row.get("price", ""),
            affiliate_url=row["affiliate_url"],
            asin=row.get("asin", ""),
            tags=tags,
            posted=(row.get("posted", "").strip().lower() in ("1", "true", "yes")),
            hook=row.get("hook", ""),
        )
