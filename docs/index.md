# Introduction

This comprehensive guide details the steps to enhance Apache Airflow's default AWS connections backend by integrating a
custom backend. This advanced setup allows Airflow to seamlessly access secrets not only within its AWS account but also
across multiple AWS accounts, utilizing [AWS Secrets Manager](https://aws.amazon.com/es/secrets-manager/).
The integration enhances security and flexibility, enabling centralized secret management across diverse cloud
environments.

## Overview

Apache Airflow's default configuration utilizes the `airflow.secrets base class for managing secrets, such as database
credentials and API keys.

<figure markdown>
  ![Image title](./images/aws-secrets-flow.jpg){ width="500" }
  <figcaption>SecretsManagerBackend Flow</figcaption>
</figure>

Our approach extends this functionality with
a [custom backend](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html),
specifically designed to retrieve secrets from AWS Secrets Manager across different AWS accounts and regions.
This solution facilitates secure and efficient secret management for complex cloud architectures.

!!! note "SecretsManagerBackend class"
    In essence, we enhance
    the [SecretsManagerBackend](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/secrets-backends/aws-secrets-manager.html)
    to enable cross-account and cross-region secrets access, thereby providing a more versatile and secure secrets
    management strategy.

<figure markdown>
  ![Image title](./images/aws-shared-secrets-flow.jpg){ width="600" }
  <figcaption>SharedSecretsManagerBackend Flow</figcaption>
</figure>
