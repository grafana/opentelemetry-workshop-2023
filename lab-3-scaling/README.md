# Lab 3. Scaling

## Contents

* [Preface](#preface)
* [3.1 - Transformation](#3.1-transformation)
* [3.2 - Load balancing](#3.2-load-balancing)


<a name="preface"></a>
## Preface

Lab 3 introduces ways to scale OpenTelemetry implementations of high complexity or high traffic.


<a name="3.1-transformation"></a>
## 3.1 - Transformation

Let's explore the fundamentals of [transforming](https://opentelemetry.io/docs/collector/transforming-telemetry/) data. You will see how to transform, clean, and enrich telemetry during its collection and transport.

> **Note** - This lab section requires the [otel-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution of the OpenTelemetry Collector.

**Why use transformations?**

Transformations provide centralized control over the processing of telemetry. This is especially useful for platform teams who must keep data quality, costs, and performance under control for multiple tenants of OpenTelemetry.

* **Quality** - Normalizing telemetry on ingest ensures higher quality usage.
* **Costs & performance** - Excluding less valuable telemetry will help control the costs of transferring, storing, and querying telemetry while optimizing the performance of ingest and queries.

**Step 1.** Review the OpenTelemetry Collector configuration for transformation: [`transformation/otel-collector-config.yaml`](transformation/otel-collector-config.yaml)

Questions to explore:

* Which processors serve the purpose of transformation?
* Which pipelines use which transformation processors?
* What benefits do those transformations offer?

**Step 2.** Run the app: `docker-compose --project-directory transformation --env-file ../env up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** Select "grafanacloud-`orgname`-logs" as the data source, "Last 15 minutes" as the time range, and run this query: `{job="java-springboot"} | json`

Questions to explore:

* What happened to the `DEBUG` logs?
* What happened to the resource attributes?

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="3.2-load-balancing"></a>
## 3.2 - Load balancing

Let's explore the fundamentals of [load balancing](https://opentelemetry.io/docs/collector/deployment/gateway/).

> **Note** - This lab section requires the [otel-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution of the OpenTelemetry Collector.

This lab uses four OpenTelemetry Collectors:

  * One serves as a load balancer or "OTLP Gateway"
  * Two receive traces and logs from the load balancer and export them to Grafana Cloud
  * One receives metrics directly from the app and exports them to Grafana Cloud

**Step 1.** Review the OpenTelemetry Collector configurations:

* [`otlp-gateway-config.yaml`](load-balancing/otlp-gateway-config.yaml) - Used by the load balancing OpenTelemetry Collector.
* [`otel-collector-config.yaml`](load-balancing/otel-collector-config.yaml) - Used by the other collectors.

Things to note:

* The [`loadbalancing`](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/loadbalancingexporter/README.md) exporter only supports traces and logs. The app sends metrics directly to an OpenTelemetry Collector that is dedicated to metrics.

**Step 2.** Review [`docker-compose.yaml`](load-balancing/docker-compose.yaml)

**Step 3.** Run the app: `docker-compose --project-directory load-balancing --env-file ../env up --build`

**Step 4.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 5.** Verify the presence of traces, metrics, and logs in Grafana Cloud. Open Grafana, click Ctrl+C or ⌘-C, type `explore` and then press Enter.

* **Traces** - Select "grafanacloud-`orgname`-traces" as the data source, "Last 15 minutes" as the time range, and click "Run query."
* **Metrics** - Select "grafanacloud-`orgname`-prom" as the data source, "Last 15 minutes" as the time range, and run this query: `{job="java-springboot"}`
* **Logs** - Select "grafanacloud-`orgname`-logs" as the data source, "Last 15 minutes" as the time range, and run this query: `{job="java-springboot"} | json`

**Step 6.** Stop the app using Ctrl+C or ⌘-C.
