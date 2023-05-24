import json

import boto3
import requests
from moto.moto_server.threaded_moto_server import ThreadedMotoServer

from airflow_aws_shared_secrets import get_aws_region


def set_up_secret(secret_name: str, content: dict) -> None:
    conn = boto3.client("secretsmanager", region_name=get_aws_region())
    conn.create_secret(Name=secret_name, SecretString=json.dumps(content))


def get_account_id() -> str:
    sts = boto3.client("sts")
    return sts.get_caller_identity()["Account"]


def set_up_moto_server(moto_server: ThreadedMotoServer) -> str:
    moto_server.start()
    address = f"http://{moto_server._ip_address}:{moto_server._port}"
    requests.post(f"{address}/moto-api/reset")
    return address
