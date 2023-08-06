from importlib import import_module
from s3_parse_url import DataSource


def import_module_if_installed(package_name: str):
    try:
        return import_module(package_name)
    except ImportError:
        return None


aiobotocore = import_module_if_installed("aiobotocore")
boto3 = import_module_if_installed("boto3")


def get_boto_client_kwargs(datasource: DataSource, **kwargs):
    return {
        "aws_access_key_id": datasource.access_key_id,
        "aws_secret_access_key": datasource.secret_access_key,
        "endpoint_url": datasource.endpoint_url,
        "region_name": datasource.region,
    }


def get_aiobotocore_client(datasource: DataSource, **kwargs):
    if aiobotocore is None:
        raise ValueError("aiobotocore not installed")
    return aiobotocore.get_session().create_client(
        "s3", **get_boto_client_kwargs(datasource, **kwargs),
    )


def get_boto3_client(datasource: DataSource, **kwargs):
    if boto3 is None:
        raise ValueError("boto3 not installed")
    return boto3.client("s3", **get_boto_client_kwargs(datasource, **kwargs))
