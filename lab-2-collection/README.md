# Lab 2. Collection

## Contents

* [Preface](#preface)
* [2.1 - OpenTelemetry Collector](#2.1-opentelemetry-collector)
* [2.2 - OpenTelemetry Collector to Grafana Stack](#2.2-grafana-agent-to-grafana-stack)
* [2.3 - Grafana Agent to Grafana Stack](#2.3-grafana-agent-to-grafana-stack)
* [2.4 - Grafana Agent to OTLP Gateway](#2.4-grafana-agent-to-otlp-gateway)


<a name="preface"></a>
## Preface

Lab 2 introduces the fundamentals of collecting and transporting data with OpenTelemetry. You will see how to collect and ship data to an external destination.


<a name="2.1-opentelemetry-collector"></a>
## 2.1 - OpenTelemetry Collector

First let's see how to collect traces, metrics, and logs with the OpenTelemetry Collector. We won't ship the data to an external destination yet. Instead the data will appear in the terminal under the container logs for the OpenTelemetry Collector.

**Step 1.** Review the OpenTelemetry Collector configuration: [`otel-collector/otel-collector-config.yaml`](otel-collector/otel-collector-config.yaml)

**Step 2.** Review [`docker-compose.yaml`](otel-collector/docker-compose.yaml)

Questions to explore:

* How are the configurations managed with environment variables?

**Step 3.** Run the app: `docker-compose --project-directory otel-collector up --build`

**Step 4.** Open the app in a web browser and visit these endpoints to generate traces, metrics, and logs:

* [http://localhost:4321/](http://localhost:4321/)
* [http://localhost:4321/error](http://localhost:4321/error)

**Step 5.** Verify the presence of traces, metrics, and logs in the output of the `otel-collector_1` container logs your terminal.

**Step 6.** Stop the app using Ctrl+C or ⌘-C.


<a name="2.2-opentelemetry-collector-to-grafana-stack"></a>
## 2.2 - OpenTelemetry Collector to Grafana Stack

> **Note** - This lab section requires the [otel-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution of the OpenTelemetry Collector.

Now let's see how the OpenTelemetry Collector ships data to an external destination. This example ships data to the Grafana Stack that includes [Tempo](https://grafana.com/oss/tempo) for traces, [Mimir](https://grafana.com/oss/mimir) for metrics, and [Loki](https://grafana.com/oss/loki) for logs.

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with traces instrumentation: `git diff --no-index otel-collector otel-collector-grafana-stack`

Questions to explore:

* How did the configuration change in [`otel-collector-config.yaml`](otel-collector-grafana-stack/otel-collector-config.yaml)?
* How did the environment variables change in [`docker-compose.yaml`](otel-collector-grafana-stack/docker-compose.yaml)?

**Step 2.** Run the app: `docker-compose --project-directory otel-collector-grafana-stack --env-file ../env up --build`

**Step 3.** Open the app in a web browser and visit these endpoints to generate traces, metrics, and logs:

* [http://localhost:4321/](http://localhost:4321/)
* [http://localhost:4321/error](http://localhost:4321/error)

**Step 4.** Verify the presence of traces, metrics, and logs in Grafana Cloud. Open Grafana, click Ctrl+C or ⌘-C, type `explore` and then press Enter.

* **Traces** - Select "grafanacloud-`orgname`-traces" as the data source, "Last 15 minutes" as the time range, and click "Run query."
* **Metrics** - Select "grafanacloud-`orgname`-prom" as the data source, "Last 15 minutes" as the time range, and run this query: `{job="java-springboot"}`
* **Logs** -  Select "grafanacloud-`orgname`-logs" as the data source, "Last 15 minutes" as the time range, and run this query: `{job="java-springboot"} | json`

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="2.3-grafana-agent-to-grafana-stack"></a>
## 2.3 - Grafana Agent to Grafana Stack

> **Note** - This lab section requires the [otel-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution of the OpenTelemetry Collector.

Now let's compare the OpenTelemetry Collector to the [Grafana Agent](https://grafana.com/docs/agent/latest/).

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with traces instrumentation: `git diff --no-index otel-collector-grafana-stack grafana-agent-grafana-stack`

Questions to explore:

* How did the environment variables change in [`docker-compose.yaml`](grafana-agent-grafana-stack/docker-compose.yaml)?

**Step 2.** Review [`grafana-agent-config.river`](grafana-agent-grafana-stack/grafana-agent-config.river)

Questions to explore:

* How are traces, metrics, and logs collected, processed, and shipped?

**Step 3.** Run the app: `docker-compose --project-directory grafana-agent-grafana-stack --env-file ../env up --build`

**Step 4.** Open the app in a web browser and visit these endpoints to generate traces, metrics, and logs:

* [http://localhost:4321/](http://localhost:4321/)
* [http://localhost:4321/error](http://localhost:4321/error)

**Step 5.** Verify the presence of traces, metrics, and logs in Grafana Cloud. Open Grafana, click Ctrl+C or ⌘-C, type `explore` and then press Enter.

* **Traces** - Select "grafanacloud-`orgname`-traces" as the data source, "Last 15 minutes" as the time range, and click "Run query."
* **Metrics** - Select "grafanacloud-`orgname`-prom" as the data source, "Last 15 minutes" as the time range, and run this query: `{job="java-springboot"}`
* **Logs** -  Select "grafanacloud-`orgname`-logs" as the data source, "Last 15 minutes" as the time range, and run this query: `{job="java-springboot"} | json`

**Step 6.** Stop the app using Ctrl+C or ⌘-C.


<a name="2.4-grafana-agent-to-otlp-gateway"></a>
## 2.4 - Grafana Agent to OTLP Gateway

The [Grafana Cloud OTLP Gateway](https://grafana.com/docs/grafana-cloud/data-configuration/otlp/send-data-otlp/) simplifies the configuration by requiring only one endpoint for traces, metrics, and logs. Let's see how this compares to shipping data to Tempo, Mimir, and Loki separately.

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with traces instrumentation: `git diff --no-index grafana-agent-grafana-stack grafana-agent-otlp-gateway`

Questions to explore:

* How did the environment variables change in [`docker-compose.yaml`](grafana-agent-otlp-gateway/docker-compose.yaml)?
* How did the configuration change in [`grafana-agent-config.river`](grafana-agent-otlp-gateway/grafana-agent-config.river)?
* How are traces, metrics, and logs collected, processed, and shipped in the new configuration?

**Step 2.** Run the app: `docker-compose --project-directory grafana-agent-otlp-gateway --env-file ../env up --build`

**Step 3.** Open the app in a web browser and visit these endpoints to generate traces, metrics, and logs:

* [http://localhost:4321/](http://localhost:4321/)
* [http://localhost:4321/error](http://localhost:4321/error)

**Step 4.** Verify the presence of traces, metrics, and logs in Grafana Cloud. Open Grafana, click Ctrl+C or ⌘-C, type `explore` and then press Enter.

* **Traces** - Select "grafanacloud-`orgname`-traces" as the data source, "Last 15 minutes" as the time range, and click "Run query."
* **Metrics** - Select "grafanacloud-`orgname`-prom" as the data source, "Last 15 minutes" as the time range, and run this query: `{job="java-springboot"}`
* **Logs** - Select "grafanacloud-`orgname`-logs" as the data source, "Last 15 minutes" as the time range, and run this query: `{job="java-springboot"} | json`

**Step 5.** Stop the app using Ctrl+C or ⌘-C.
