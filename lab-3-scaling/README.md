# Lab 3. Scaling

## Contents

* [Preface](#preface)
* [3.1 - Transformation](#3.1-transformation)
* [3.2 - Load balancing](#3.2-load-balancing)
* [3.3 - Sampling](#3.3-sampling)


<a name="preface"></a>
## Preface

Lab 3 introduces ways to scale OpenTelemetry implementations of high complexity or high traffic.


<a name="3.1-transformation"></a>
## 3.1 - Transformation

> **Note** - This lab section requires the [otel-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution of the OpenTelemetry Collector.

Let's explore the fundamentals of [transforming](https://opentelemetry.io/docs/collector/transforming-telemetry/) data. You will see how to transform, clean, and enrich telemetry during its collection and transport.

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

> **Note** - This lab section requires the [otel-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution of the OpenTelemetry Collector.

Let's explore the fundamentals of [load balancing](https://opentelemetry.io/docs/collector/deployment/gateway/).

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


<a name="3.3-sampling"></a>
## 3.3 - Sampling

> **Note** - This lab section requires the [otel-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) distribution of the OpenTelemetry Collector.

Let's explore the fundamentals of [sampling](https://opentelemetry.io/docs/concepts/sampling/). Sampling limits the amount of traces that reaches its destination. This helps keep costs under control, and helps optimize the performance of ingest and queries.

There are two forms of sampling:

* **Head sampling** makes probabilistic decisions on whether to keep traces. If you define a policy to sample 10% of all traces, then there is a 10% chance that the OpenTelemetry Collector will sample any given trace. This is easy to implement and uses compute resources efficiently.

* **Tail sampling** makes policy-based decisions on whether to keep traces once all spans have been captured. You could choose to sample 100% of traces containing errors in any child span, while keeping just a representative sample of everything else. This gives you finer control over what gets kept, possibly optimizing costs and performance better than head sampling. However, it requires queueing many spans in memory and waiting for all spans of a given trace to arrive. This can require significantly more compute resources for the OpenTelemetry Collector(s), and adds latency to the ingest process.


### Head sampling

Let's use the [probabilistic_sampler](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/probabilisticsamplerprocessor) processor to implement a strategy that samples 20% of all traces.

**Step 1.** Review the OpenTelemetry Collector configuration: [`otel-collector-config.yaml`](head-sampling/otel-collector-config.yaml)

**Step 2.** Run the app: `docker-compose --project-directory head-sampling --env-file ../env up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** Verify the presence of traces and logs in Grafana Cloud. Open Grafana, click Ctrl+C or ⌘-C, type `explore` and then press Enter.

* **Traces** - Select "grafanacloud-`orgname`-traces" as the data source, "Last 15 minutes" as the time range, and click "Run query."
* **Logs** - Select "grafanacloud-`orgname`-logs" as the data source, "Last 15 minutes" as the time range, and run this query: `{job="java-springboot"} | json`

Keep refreshing the app in your web browser. For every 10 page loads, there should be approximately 2 traces that appear in Grafana.

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


### Tail sampling

Let's use the [tail_sampling](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor) processor to implement a strategy that samples 100% of traces that have errors in any of its child spans, and samples 20% of all other traces.

**Step 1.** Review the OpenTelemetry Collector configuration: [`otel-collector-config.yaml`](tail-sampling/otel-collector-config.yaml)

**Step 2.** Run the app: `docker-compose --project-directory tail-sampling --env-file ../env up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** Verify the presence of traces in Grafana Cloud. Open Grafana, click Ctrl+C or ⌘-C, type `explore` and then press Enter. Select "grafanacloud-`orgname`-traces" as the data source, "Last 15 minutes" as the time range, and click "Run query."

Perform two tests in your web browser:

* Reload the `/` page in your web browser 10 times: [http://localhost:4321/](http://localhost:4321/)
* Reload the `/error` page in your web browser 10 times: [http://localhost:4321/](http://localhost:4321/)

After ~5 seconds for each test, you should see 10 traces for `java-springboot GET /error` and ~2 traces for `java-springboot GET /` display in Grafana. That's because the tail sampling policies we defined in [`otel-collector-config.yaml`](tail-sampling/otel-collector-config.yaml) will sample 100% of traces having an `ERROR` status code and 20% of all other traces.

Questions to explore:

* What are the trade-offs for having a longer or shorter `decision_wait` time in [`otel-collector-config.yaml`](tail-sampling/otel-collector-config.yaml)?

**Step 5.** Stop the app using Ctrl+C or ⌘-C.
