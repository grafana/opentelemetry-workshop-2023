# OpenTelemetry Workshop

*OTel makes it easy! Here's how.*

* [Prerequisites](#prerequisites)
* [Lab 1 - Instrumentation](lab-1-instrumentation)
* [Lab 2 - Collection](lab-2-collection)
* [Lab 3 - Scaling](lab-3-scaling)


<a name="prerequisites"></a>
## Prerequisites


<a name="1-prepare-your-local-environment"></a>
### 1. Prepare your local environment


<a name="1.1-install-dependencies"></a>
#### 1.1. Install dependencies

You will need a laptop or VM with the following software installed (use the links for installation instructions):

* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

Verify your installations by running these commands in your terminal:

* `git --version` (expected output: `2.32.1` or higher)
* `docker --version` (expected output: `20.10.12` or higher)
* `docker-compose --version` (expected output: `1.29.2` or higher)


<a name="1.2-clone-this-repo"></a>
#### 1.2. Clone this repo

You will need to clone this repository:

```sh
git clone https://github.com/grafana/opentelemetry-workshop.git
```


<a name="1.3-confirm-internet-access"></a>
#### 1.3. Confirm internet access

Your laptop or VM will need outbound public internet access to these hostnames, protocols, and ports:

|Hostname|Protocol|Port|
|--------|--------|----|
|*.docker.com|HTTPS|443|
|*.docker.io|HTTPS|443|
|*.github.com|HTTPS|443|
|*.grafana.com|HTTPS|443|
|*.grafana.net|HTTPS|443|


<a name="2-prepare-grafana-cloud"></a>
### 2. Prepare Grafana Cloud

You will need a Grafana Cloud stack using the free tier.


<a name="2.1-register-an-account"></a>
#### 2.1. Register an account

1. Register an account: [https://grafana.com/auth/sign-up/create-user](https://grafana.com/auth/sign-up/create-user)
1. Acknowledge the confirmation email.


<a name="2.2-provision-a-stack"></a>
#### 2.2. Provision a stack

1. Sign into Grafana Cloud: [https://grafana.com/auth/sign-in/](https://grafana.com/auth/sign-in/)
1. On the left navigation menu, click `+ Add Stack` and follow the prompts.
1. Your stack will be ready in less than a minute.


<a name="2.3-create-a-token"></a>
#### 2.3. Create a token

1. Sign into Grafana Cloud: [https://grafana.com/auth/sign-in/](https://grafana.com/auth/sign-in/)
1. On the left navigation menu, click `Access Policies` and then click `Create access policy`.
1. Give it a name, select `(all stacks)` as your realm, and select the checkboxes under `Write` for the `metrics`, `logs`, and `traces` resources.
1. Click `Create`
1. Click `Add token` under your newly created access policy.
1. Give your token a name and then click `Create`.
1. Click `Copy to Clipboard` to copy the token. You won't be able to see it again. If you lose it, you can create a new one.
1. Save your token in your copy of the `./env` file in this repo as the value of `GRAFANA_CLOUD_TOKEN`.

Example:

```sh
# Grafana Cloud
GRAFANA_CLOUD_TOKEN=paste_your_token_here
...
```


<a name="2.4-obtain-environment-variables"></a>
#### 2.4. Obtain environment variables

Once you have provisioned a stack, you will need to update your local copy of the [`./env`](env) file from this repo with the following values.

1. Sign into Grafana Cloud: [https://grafana.com/auth/sign-in/](https://grafana.com/auth/sign-in/)
1. On the left navigation menu, click the link to your stack.
1. Click the `Details` buttons under "Grafana," "Loki," "Prometheus," and "Tempo" to obtain the following values for your [`./env`](env) file:

|Environment Variable|Instructions|
|--------------------|------------|
|**`GRAFANA_CLOUD_TOKEN`**|Completed in [Section 2.3](#2.3-create-a-token).|
|**`GRAFANA_CLOUD_INSTANCE_ID`**|Under **Grafana > Details**, copy the value of "Instance ID".<br/><br/>Example: `123456`|
|**`GRAFANA_CLOUD_REGION`**|Under **Grafana > Details**, copy the value of "Zone" without the parentheses.<br/><br/>Example: `prod-us-central-0`|
|**`GRAFANA_STACK_LOKI_URL`**|Under **Loki > Details**, copy the value of "URL" and append it with `/loki/api/v1/push`<br/><br/>Example: `https://logs-prod-017.grafana.net/loki/api/v1/push`|
|**`GRAFANA_STACK_LOKI_USERNAME`**|Under **Loki > Details**, copy the value of "User".<br/><br/>Example: `123456`|
|**`GRAFANA_STACK_PROMETHEUS_URL`** |Under **Prometheus > Details**, copy the value of "Remote Write Endpoint".<br/><br/>Example: `https://prometheus-us-central1.grafana.net/api/prom/push`|
|**`GRAFANA_STACK_PROMETHEUS_USERNAME`**|Under **Prometheus > Details**, copy the value of "Username / Instance ID".<br/><br/>Example: `123456`|
|**`GRAFANA_STACK_TEMPO_URL`**|Under **Tempo > Details**, copy the value of "URL" and replace `/tempo` with `:443`<br/><br/>Example: `https://tempo-us-central1.grafana.net:443`|
|**`GRAFANA_STACK_TEMPO_USERNAME`**|Under **Tempo > Details**, copy the value of "User".<br/><br/>Example: `123456`|
