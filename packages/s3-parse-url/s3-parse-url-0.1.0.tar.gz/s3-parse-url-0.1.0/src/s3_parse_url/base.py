from typing import List, Optional
from urllib.parse import parse_qs, urlparse

from s3_parse_url.exceptions import UnsupportedStorage


class DataSource:
    allowed_schemas: List[str] = ["s3"]
    default_endpoint: str = None
    default_region: str = None

    def __init__(self, dsn: str):
        self._dsn = dsn
        self._raw_bits = None
        self._parsed_bits = {}
        self._parse()

    def __str__(self):
        return self._dsn

    @property
    def endpoint_url(self) -> Optional[str]:
        return self._parsed_bits["endpoint_url"]

    @property
    def bucket_name(self) -> str:
        return self._parsed_bits["bucket_name"]

    @property
    def region(self) -> str:
        return self._parsed_bits["region"]

    @property
    def access_key_id(self) -> str:
        return self._parsed_bits["aws_access_key_id"]

    @property
    def secret_access_key(self) -> str:
        return self._parsed_bits["aws_secret_access_key"]

    def _parse(self):
        self._raw_bits = urlparse(self._dsn)
        self._check_if_compatible()
        self._parsed_bits.update(**{
            "aws_secret_access_key": self._parse_secret_access_key(),
            "aws_access_key_id": self._parse_access_key_id(),
            "endpoint_url": self._parse_endpoint_url(),
            "bucket_name": self._parse_bucket_name(),
            "region": self._parse_region_name(),
        })

    def _parse_access_key_id(self):
        return self._raw_bits.username

    def _parse_secret_access_key(self):
        return self._raw_bits.password

    def _parse_endpoint_url(self):
        endpoint_url = None
        if self.default_endpoint is not None:
            return self.default_endpoint
        if self._raw_bits.hostname and self._raw_bits.path:
            endpoint_url = "https://" + self._raw_bits.hostname
        if self._raw_bits.port and isinstance(self._raw_bits.port, int):
            endpoint_url += ":" + str(self._raw_bits.port)
        return endpoint_url

    def _parse_region_name(self) -> str:
        region = parse_qs(self._raw_bits.query).get("region")
        if region and region[0]:
            return region[0]
        else:
            return self.default_region

    def _parse_bucket_name(self) -> str:
        bucket_name = self._raw_bits.path.strip("/").split("/")[0]
        if not bucket_name:
            bucket_name = self._raw_bits.hostname
        return bucket_name

    def _check_if_compatible(self):
        scheme = self._raw_bits.scheme
        if not self.allowed_schemas:
            return
        if not scheme:
            raise UnsupportedStorage("Unable to detect schema")
        if scheme.lower() not in self.allowed_schemas:
            raise UnsupportedStorage("Unsupported schema " + scheme +
                                     " for the backend")
