## Prerequisites

- Apache Airflow 2.x
- Access to the AWS accounts from which you want to fetch secrets
  _(
  See: [Permissions to AWS Secrets Manager secrets for users in a different account](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples_cross.html))_
- Permissions to create and manage secrets in AWS Secrets Manager
- Access to edit your Airflow Helm properties.

## Helm configuration

The documentation is based on [Airflow Helm Chart (Users Community)](https://airflow-helm.github.io/charts/), but it
should apply to other existing Airflow Helms, since the configuration would be handled via ENV vars or the config file.

!!! note extraPipPackages
    Add the **airflow-aws-shared-secrets** package in the `extraPipPackages` section, so the library is deployed into
    the airflow workers pods.

## Configure Airflow to use our Custom Backend

To use the AWs Shared Secrets Backed in Airflow, we must update the airflow.cfg file or set the corresponding
environment variable:

Edit airflow.cfg:

```toml
[secrets]
backend = 'airflow_aws_shared_secrets.secret_manager.SharedSecretsManagerBackend'
```

Or, set an environment variable:

```toml
### [secrets]
AIRFLOW__SECRETS__BACKEND: 'airflow_aws_shared_secrets.secret_manager.SharedSecretsManagerBackend'
AIRFLOW__SECRETS__BACKEND_KWARGS: '{"connections_prefix": "airflow/connections/", "connections_prefix_shared" : "airflow/connections/shared", "shared_account": "123581321", "aws_region": "eu-central-1"}'
```

## Backend properties

We expect the following extra properties to be defined within the `backend_kwargs` in addition to
the [native ones](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/secrets-backends/aws-secrets-manager.html#aws-secrets-manager-backend).

- shared_account: Account ID from the aws-account you are sharing the main secrets.
- aws_region: The AWs Region from where the secrets are being stored in.

!!! note Conclusion
    By following these steps, you've successfully overridden the default AWS connections backend in Airflow with a custom one that allows accessing secrets from other AWS accounts.
    This setup enhances your Airflow project's flexibility and security when managing cross-account AWS resources.


## Specs Example
```yaml
apiVersion: v2
kind: HelmRelease
metadata:
  name: airflow
spec:
  releaseName: airflow
  chart:
    spec:
      chart: airflow
      version: 8.8.0
  interval: 2h0m0s
  install:
    remediation:
      retries: 3
  values: # https://github.com/airflow-helm/charts/blob/main/charts/airflow/values.yaml
    airflow:
      image:
        repository: apache/airflow
        tag: 2.8.1-python3.10 # https://hub.docker.com/r/apache/airflow/tags
      executor: CeleryExecutor
      extraPipPackages:
        - "apache-airflow-providers-amazon==8.13.0"
        - "airflow-aws-shared-secrets==0.0.5" # https://github.com/afranzi/airflow-aws-shared-secrets
      config:
        ### ref: https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html
        ### [core]
        AIRFLOW__CORE__CHECK_SLAS: 'False'
        AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG: 1
        AIRFLOW__CORE__MIN_SERIALIZED_DAG_UPDATE_INTERVAL: 150

        ### [secrets]
        AIRFLOW__SECRETS__BACKEND: 'airflow_aws_shared_secrets.secret_manager.SharedSecretsManagerBackend'
        AIRFLOW__SECRETS__BACKEND_KWARGS: '{"connections_prefix": "aily/${tenant_name}/${environment}/airflow", "shared_account": "258781458051", "connections_prefix_shared" : "aily/coreproduct/airflow", "aws_region": "eu-central-1"}'

      ## Extra environment variables for the airflow Pods
      ## [FAQ] https://github.com/airflow-helm/charts/blob/main/charts/airflow/docs/faq/kubernetes/mount-environment-variables.md
      extraEnv:
        ...

    serviceAccount:
      create: true
      annotations:
        eks.amazonaws.com/role-arn: ${airflow_irsa}
```

## Links of Interest

Check [configurations-ref](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) for more
Airflow configuration possibilities.
