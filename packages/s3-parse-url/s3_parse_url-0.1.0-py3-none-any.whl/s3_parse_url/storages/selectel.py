from s3_parse_url.base import DataSource


class SelectelStorage(DataSource):
    allowed_schemas = ["selectel"]
    default_region = "ru-1"
    default_endpoint = "https://s3.selcdn.ru"
