## Prerequisites

- **Apache Airflow 2.x:** Ensure Airflow is updated to at least version 2.0.
- **AWS Account Access:** You need access to the AWS accounts from which secrets will be fetched
  _(
  See: [Permissions to AWS Secrets Manager secrets for users in a different account](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples_cross.html))_
- **Permissions**: Adequate permissions to manage secrets within AWS Secrets Manager and configure IAM policies.
- **Helm:** Familiarity with Helm for deploying and managing Kubernetes applications, as this guide uses the Airflow
  Helm Chart.

## Helm configuration

This documentation leverages the [Airflow Helm Chart (Users Community)](https://airflow-helm.github.io/charts/). The
instructions should be universally applicable across different Helm deployments, thanks to the flexibility of
environment variables and configuration files.

!!! note "extraPipPackages"
    Ensure the **airflow-aws-shared-secrets** package is included in the `extraPipPackages` section of your Helm values.
    This ensures the custom library is deployed into the Airflow worker pods, enabling them to interact with the custom
    backend.

## Configure Airflow to use our Custom Backend

To activate the AWS Shared Secrets Backend in Airflow, adjust either the `airflow.cfg` file directly or set the
appropriate environment variables:

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

The custom backend expects additional properties within `backend_kwargs` enhancing functionality beyond the native capabilities in addition to
the [native ones](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/secrets-backends/aws-secrets-manager.html#aws-secrets-manager-backend).

- shared_account: Specifies the AWS account ID where the primary secrets are stored. This facilitates cross-account secret access.
- aws_region: Defines the AWS region of the secrets manager, ensuring the backend can retrieve secrets from the specified geographical location.

!!! info "Conclusion"
    By following these steps, you've successfully overridden the default AWS connections backend in Airflow with a custom
    one that allows accessing secrets from other AWS accounts.
    This setup enhances your Airflow project's flexibility and security when managing cross-account AWS resources.

## Implementing Best Practices
When configuring and using the custom backend, adhere to the following best practices for security and efficiency:

- **Minimal IAM Permissions:** Assign only the necessary permissions to the IAM roles used by Airflow, following the principle of least privilege.
- **Secure Secret Storage:** Ensure that all secrets stored in AWS Secrets Manager are encrypted at rest using keys managed by AWS KMS.
- **Regular Audits:** Periodically review AWS access logs and Airflow access patterns to ensure compliance with security policies.

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
