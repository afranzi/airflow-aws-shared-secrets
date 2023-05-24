import unittest

from moto import mock_secretsmanager, mock_sts

from airflow_aws_shared_secrets import get_aws_region
from airflow_aws_shared_secrets.secret_manager import SharedSecretsManagerBackend
from tests import auto_inject_fixtures
from tests.test_helpers import get_account_id, set_up_moto_server, set_up_secret


@mock_sts
@mock_secretsmanager
@auto_inject_fixtures("moto_server")
class TestSharedSecretsManagerBackend(unittest.TestCase):
    def setUp(self) -> None:
        self.moto_server_address = set_up_moto_server(self.moto_server)  # type: ignore

    def tearDown(self) -> None:
        self.moto_server.stop()  # type: ignore

    def test_secret_access(self) -> None:
        shared_prefix = "airflow/shared/connections"
        connection = {"host": "https://github.com/afranzi", "login": "potato", "port": 42}
        set_up_secret(f"{shared_prefix}/my_secret", connection)

        config = {
            "connections_prefix": "airflow/connections",
            "shared_account": get_account_id(),
            "connections_prefix_shared": shared_prefix,
            "region_name": get_aws_region(),
            "endpoint_url": self.moto_server_address,
        }
        shared_secret_manager_backend = SharedSecretsManagerBackend(**config)

        result = shared_secret_manager_backend.get_connection(conn_id="my_secret")
        self.assertIsNotNone(result)
        if result:
            self.assertEqual(connection["host"], result.host)
            self.assertEqual(connection["login"], result.login)
            self.assertEqual(connection["port"], result.port)
