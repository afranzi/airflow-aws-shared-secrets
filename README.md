# airflow-aws-shared-secrets

SecretsManagerBackend with cross-account access.

Expected properties where:
- shared_account: account_id from your core aws-account
- aws_region: aws_region where the core secrets are stored in

```json
{
    "connections_prefix": "airflow/connections/${environment}",
    "connections_prefix_shared" : "airflow/core/connections/${environment}",
    "shared_account": "123456789012",
    "aws_region": "eu-central-1"
}
```

## Usage

We recommend setting up the SharedSecretsManager in
the [Airflow Helm](https://github.com/airflow-helm/charts/blob/main/charts/airflow/values.yaml) by configuring
the following config values.

```toml
### [secrets]
AIRFLOW__SECRETS__BACKEND: 'airflow_aws_shared_secrets.secret_manager.SharedSecretsManagerBackend'
AIRFLOW__SECRETS__BACKEND_KWARGS: '{"connections_prefix": "airflow/connections/${environment}", "connections_prefix_shared" : "airflow/core/connections/${environment}", "shared_account": "<my_core_aws_account_id>", "aws_region": "eu-central-1"}'
```

Check [configurations-ref](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) for more
Airflow configuration possibilities.
