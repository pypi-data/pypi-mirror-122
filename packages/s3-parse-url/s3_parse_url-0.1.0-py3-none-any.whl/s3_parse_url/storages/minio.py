from s3_parse_url.base import DataSource

# See https://docs.min.io/docs/aws-cli-with-minio.html
#
# A notable thing: according to the docs, the default region
# should be "us-east-1"


class Minio(DataSource):
    allowed_schemas = ["minio"]
    default_region = "us-east-1"

    def _parse_endpoint_url(self) -> str:
        endpoint_url = super()._parse_endpoint_url()
        return endpoint_url
