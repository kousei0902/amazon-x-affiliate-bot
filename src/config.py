import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AmazonConfig:
    associate_tag: str
    access_key: str
    secret_key: str
    country: str

    @property
    def is_configured(self) -> bool:
        return bool(self.access_key and self.secret_key and self.associate_tag)


@dataclass(frozen=True)
class XConfig:
    api_key: str
    api_secret: str
    access_token: str
    access_secret: str

    @property
    def is_configured(self) -> bool:
        return bool(
            self.api_key
            and self.api_secret
            and self.access_token
            and self.access_secret
        )


@dataclass(frozen=True)
class AppConfig:
    amazon: AmazonConfig
    x: XConfig
    posts_per_run: int


def load_config() -> AppConfig:
    amazon = AmazonConfig(
        associate_tag=os.getenv("AMAZON_ASSOCIATE_TAG", ""),
        access_key=os.getenv("AMAZON_ACCESS_KEY", ""),
        secret_key=os.getenv("AMAZON_SECRET_KEY", ""),
        country=os.getenv("AMAZON_COUNTRY", "JP"),
    )
    x = XConfig(
        api_key=os.getenv("X_API_KEY", ""),
        api_secret=os.getenv("X_API_SECRET", ""),
        access_token=os.getenv("X_ACCESS_TOKEN", ""),
        access_secret=os.getenv("X_ACCESS_SECRET", ""),
    )
    posts_per_run = int(os.getenv("POSTS_PER_RUN", "1"))
    return AppConfig(amazon=amazon, x=x, posts_per_run=posts_per_run)
