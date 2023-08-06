from s3_parse_url.base import DataSource


class YandexCloud(DataSource):
    default_endpoint = "https://storage.yandexcloud.net"
    default_region = "ru-central1"
    allowed_schemas = ["yandex"]
