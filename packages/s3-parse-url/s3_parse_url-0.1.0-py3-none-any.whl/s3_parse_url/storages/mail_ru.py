from s3_parse_url.base import DataSource


class IceBox(DataSource):
    default_region = "ru-msk"
    default_endpoint = "https://ib.bizmrg.com"
    allowed_schemas = ["mailru+ice"]


class HotBox(DataSource):
    default_region = "ru-msk"
    default_endpoint = "https://hb.bizmrg.com"
    allowed_schemas = ["mailru", "mailru+hot"]
