from s3_parse_url.base import DataSource


class AmazonS3(DataSource):
    allowed_schemas = ["s3"]
    default_region = "us-east-1"
