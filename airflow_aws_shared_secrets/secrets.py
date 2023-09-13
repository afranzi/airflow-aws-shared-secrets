import re

import boto3
from boto3 import Session
from botocore.exceptions import ClientError
from mypy_boto3_secretsmanager import SecretsManagerClient


def aws_session(region_name: str | None = None) -> Session:
    return boto3.session.Session(region_name=region_name)


def secrets_client(region_name: str | None = None) -> SecretsManagerClient:
    return aws_session(region_name).client(service_name="secretsmanager")


def get_region_from_secret(secret_name: str) -> str | None:
    arn_regex = re.compile(
        r"arn:aws:secretsmanager:(?P<region>[\w-]+):(?P<account_id>\d{12}):secret:(?P<secret_name>.+)",
    )
    search_result = arn_regex.search(secret_name)
    search_groups = search_result.groupdict() if search_result else {}
    return search_groups.get("region")


def get_secret(region_name: str, secret_name: str) -> str | None:
    region_name = get_region_from_secret(secret_name) or region_name
    client = secrets_client(region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return response.get("SecretString")
