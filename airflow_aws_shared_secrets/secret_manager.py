from typing import Any

from airflow.providers.amazon.aws.secrets.secrets_manager import SecretsManagerBackend

from airflow_aws_shared_secrets import get_aws_region


class SharedSecretsManagerBackend(SecretsManagerBackend):
    def __init__(
        self,
        shared_account: str,
        connections_prefix_shared: str = "airflow/connections",
        aws_region: str | None = None,
        **kwargs: Any,
    ):
        SecretsManagerBackend.__init__(self, **kwargs)
        self.aws_region = aws_region or get_aws_region()
        self.shared_account = shared_account
        self.connections_prefix_shared = connections_prefix_shared

    @staticmethod
    def build_secret_arn_prefix(aws_region: str, account_id: str, prefix: str) -> str:
        return f"arn:aws:secretsmanager:{aws_region}:{account_id}:secret:{prefix}"

    def _get_secret(self, path_prefix: str, secret_id: str, lookup_pattern: str | None) -> str | None:
        secret = SecretsManagerBackend._get_secret(
            self,
            path_prefix=self.connections_prefix,
            secret_id=secret_id,
            lookup_pattern=self.connections_lookup_pattern,
        )

        if secret is None:
            path_prefix = self.build_secret_arn_prefix(
                aws_region=self.aws_region,
                account_id=self.shared_account,
                prefix=self.connections_prefix_shared,
            )
            secret = SecretsManagerBackend._get_secret(
                self,
                path_prefix=path_prefix,
                secret_id=secret_id,
                lookup_pattern=self.connections_lookup_pattern,
            )
        return secret
