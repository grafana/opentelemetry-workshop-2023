# OpenTelemetry Workshop

*OTel is easy! Here's how.*

* [Lab 1 - Instrumentation](lab-1)
* [Lab 2 - Collection & Transport](lab-2)
* [Lab 3 - Usage](lab-3)

## Prerequisites

You will need a laptop or VM with the following software installed (use the links for installation instructions):

* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

Verify your installations by running these commands in your terminal:

* `git --version` (expected output: `2.32.1` or higher)
* `docker --version` (expected output: `20.10.12` or higher)
* `docker-compose --version` (expected output: `1.29.2` or higher)

Your laptop or VM will need outbound public internet access to these hostnames, protocols, and ports:

* *.docker.com (HTTPS/443)
* *.docker.io (HTTPS/443)
* *.github.com (HTTPS/443)
* *.grafana.com (HTTPS/443)
* *.grafana.net (HTTPS/443)

Lastly, you will need a Grafana Cloud stack using the free tier.

* Register an account: [https://grafana.com/auth/sign-up/create-user](https://grafana.com/auth/sign-up/create-user)
* Acknowledge the confirmation email.
* Sign into Grafana Cloud: [https://grafana.com/auth/sign-in/](https://grafana.com/auth/sign-in/)
* On the left navigation menu, click "+Add Stack" and follow the prompts.
