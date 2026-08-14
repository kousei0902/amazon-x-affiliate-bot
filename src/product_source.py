import csv
from pathlib import Path

from .models import Product

FIELDNAMES = ["id", "asin", "name", "price", "affiliate_url", "tags", "posted", "hook"]


def load_products(csv_path: Path) -> list[Product]:
    if not csv_path.exists():
        return []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [Product.from_row(row) for row in reader]


def load_pending(csv_path: Path) -> list[Product]:
    return [p for p in load_products(csv_path) if not p.posted]


def save_products(csv_path: Path, products: list[Product]) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for p in products:
            writer.writerow(
                {
                    "id": p.id,
                    "asin": p.asin,
                    "name": p.name,
                    "price": p.price,
                    "affiliate_url": p.affiliate_url,
                    "tags": "|".join(p.tags),
                    "posted": "true" if p.posted else "false",
                    "hook": p.hook,
                }
            )


def mark_posted(csv_path: Path, product_id: str) -> None:
    products = load_products(csv_path)
    for p in products:
        if p.id == product_id:
            p.posted = True
    save_products(csv_path, products)
