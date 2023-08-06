from urllib.parse import urlparse

from s3_parse_url.exceptions import UnsupportedStorage
from s3_parse_url.storages.amazon import AmazonS3
from s3_parse_url.base import DataSource
from s3_parse_url.storages.mail_ru import HotBox, IceBox
from s3_parse_url.storages.minio import Minio
from s3_parse_url.storages.selectel import SelectelStorage
from s3_parse_url.storages.yandex import YandexCloud

__all__ = ["parse_s3_dsn", "parse_s3_url", "UnsupportedStorage"]


SUPPORTED_STORAGES = {
    "s3": AmazonS3,
    "selectel": SelectelStorage,
    "mailru": HotBox,
    "mailru+hot": HotBox,
    "mailru+ice": IceBox,
    "minio": Minio,
    "yandex": YandexCloud,
}


def parse_s3_dsn(dsn: str) -> DataSource:
    """
    Parses a datasource string to a dict of arguments compatible with
    """
    try:
        cls = SUPPORTED_STORAGES[urlparse(dsn).scheme.lower()]
    except (AttributeError,
            KeyError):
        raise UnsupportedStorage()
    else:
        return cls(dsn)


parse_s3_url = parse_s3_dsn
