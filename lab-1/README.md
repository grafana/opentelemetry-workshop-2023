# Lab 1. Instrumentation

## Contents

* [Preface](#preface)
* [Lab 1.1 - No instrumentation](#lab-1.1-no-instrumentation)
* [Lab 1.2 - Traces instrumentation](#lab-1.2-traces-instrumentation)
* [Lab 1.3 - Metrics instrumentation](#lab-1.3-metrics-instrumentation)
* [Lab 1.4 - Logs instrumentation](#lab-1.4-logs-instrumentation)
* [Lab 1.5 - Complete instrumentation](#lab-1.5-complete-instrumentation)
* [Lab 1.6 - Automatic instrumentation for Java](#lab-1.6-automatic-instrumentation-for-java)
* [Retrospective](#retrospective)


<a name="preface"></a>
## Preface

Lab 1 introduces the fundamentals of [instrumentation](https://opentelemetry.io/docs/instrumentation/) with OpenTelemetry.

You will see how to instrument traces, metrics, and logs with a clear and systematic set of instructions. Lab 1 does not ship data to external destinations – that is covered in [Lab 2](.lab-2). You will see the data in your terminal in Lab 1.

The lab uses an app implemented in two programming languages and app frameworks:

* **Python** using the [Flask](https://flask.palletsprojects.com/en/2.3.x/) framework ([`python-flask`](python-flask))
* **Java** using the [Spring Boot](https://spring.io/projects/spring-boot) framework ([`java-springboot`](java-springboot))

Each app contains five variants:

* **Bare** - No instrumentation
* **Traces** - Traces instrumentation
* **Metrics** - Metrics instrumentation
* **Logs** - Logs instrumentation
* **Complete** - All three instrumentations with correlations

The lab will run commands in the terminal. You will need to navigate into the `lab-1` directory and run the commands from there.

Using the `git diff` command, you can compare a **bare** app with one of its instrumentation variants. This lets you see exactly what steps were needed to instrument traces, metrics, or logs. Nothing more, nothing less.

Example:

```sh
git diff --no-index python-flask/1-bare python-flask/2-traces
```

To run one of the apps, navigate to `lab-1` and run the command below after changing the value of `path_to_app_directory`:

```sh
APP=path_to_app_directory docker-compose up --build
```

Example:

```sh
APP=python-flask/5-complete docker-compose up --build
```

This command builds and runs the app on port `4321`. You can view the running app in your web browser at [http://localhost:4321/](http://localhost:4321/) and then view the activity in your terminal.

You can control the app using these endpoints:

* [http://localhost:4321/](http://localhost:4321/) - Responds with `ok`
* [http://localhost:4321/error](http://localhost:4321/error) - Responds with an error message after attempting to divide by zero

<a name="lab-1.1-no-instrumentation"></a>
## Lab 1.1 - No instrumentation

Before instrumenting the app, let's see how it behaves on its own. This will help us understand the effect of each instrumentation in the next sections of the lab.

**Step 1.** Review the app code in a text editor: [`python-flask/1-bare/app.py`](python-flask/1-bare/app.py)

**Step 2.** Run the app: `APP=python-flask/1-bare docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/) - Notice that the app responds with `ok` for any message.

**Step 4.** View the app logs in your terminal. Notice that the app writes logs when the app starts, and when the app handles a request in the web browser.

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="lab-1.2-traces-instrumentation"></a>
## Lab 1.2 - Traces instrumentation

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with traces instrumentation: `git diff --no-index python-flask/1-bare python-flask/2-traces`

Questions to explore:

* What dependencies were added? Note: Python dependencies are declared in the [`requirements.txt`](python-flask/2-traces/requirements.txt) file.
* How did the code change in [`app.py`](python-flask/2-traces/app.py)?
* How did the environment variables change in [`Dockerfile`](python-flask/2-traces/Dockerfile)?

Things to know:

* The app uses a `BatchSpanProcessor` for each exporter.
* The app uses a `ConsoleSpanExporter` to send spans to the terminal (i.e. `stdout`).
* The app uses `FlaskInstrumentor` to auto-instrument the web app framework.

Best practices:

* `ConsoleSpanExporter` is a great tool when implementing instrumentations in development, because it rules out any variables downstream of the app (e.g. networking issues or database issues) when troubleshooting your implementation. In production, you can omit `ConsoleSpanExporter` to prevent noisy logs.

**Step 2.** Run the app: `APP=python-flask/2-traces docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal. Notice that the traces appear in the terminal.

<details>
<summary>View sample trace</summary>

```json
{
  "name": "/",
  "context": {
    "trace_id": "0x57f89f02eeb085a97410dc5419951140",
    "span_id": "0xada3d31bea4f57d4",
    "trace_state": "[]"
  },
  "kind": "SpanKind.SERVER",
  "parent_id": null,
  "start_time": "2023-06-26T20:27:37.834969Z",
  "end_time": "2023-06-26T20:27:37.837844Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {
    "http.method": "GET",
    "http.server_name": "0.0.0.0",
    "http.scheme": "http",
    "net.host.port": 4321,
    "http.host": "localhost:4321",
    "http.target": "/",
    "net.peer.ip": "172.26.0.1",
    "http.user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "net.peer.port": 63836,
    "http.flavor": "1.1",
    "http.route": "/",
    "http.status_code": 200
  },
  "events": [],
  "links": [],
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.18.0",
      "service.name": "python-flask"
    },
    "schema_url": ""
  }
}
```
</details>

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="lab-1.3-metrics-instrumentation"></a>
## Lab 1.3 - Metrics instrumentation

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with metrics instrumentation: `git diff --no-index python-flask/1-bare python-flask/3-metrics`

Questions to explore:

* What dependencies were added? Note: Python dependencies are declared in the [`requirements.txt`](python-flask/3-metrics/requirements.txt) file.
* How did the code change in [`app.py`](python-flask/3-metrics/app.py)?
* How did the environment variables change in [`Dockerfile`](python-flask/3-metrics/app.py)?
* How do these changes compare with the traces instrumentation?

Things to know:

* The app uses a `PeriodicExportingMetricReader` for each exporter. Notice the configurable export interval that is set to `5000ms`.
* The app uses a `ConsoleMetricExporter` that serves the same purpose as the `ConsoleSpanExporter` from the traces instrumentation.

**Step 2.** Run the app: `APP=python-flask/3-metrics docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal. Notice that the metrics appear in the terminal every 5 seconds, as instructed by the `5000ms` export interval.

<details>
<summary>View sample metrics</summary>

```json
{
  "resource_metrics": [
    {
      "resource": {
        "attributes": {
          "telemetry.sdk.language": "python",
          "telemetry.sdk.name": "opentelemetry",
          "telemetry.sdk.version": "1.18.0",
          "service.name": "python-flask"
        },
        "schema_url": ""
      },
      "scope_metrics": [
        {
          "scope": {
            "name": "opentelemetry.instrumentation.flask",
            "version": "0.39b0",
            "schema_url": ""
          },
          "metrics": [
            {
              "name": "http.server.active_requests",
              "description": "measures the number of concurrent HTTP requests that are currently in-flight",
              "unit": "requests",
              "data": {
                "data_points": [
                  {
                    "attributes": {
                      "http.method": "GET",
                      "http.host": "localhost:4321",
                      "http.scheme": "http",
                      "http.flavor": "1.1",
                      "http.server_name": "0.0.0.0"
                    },
                    "start_time_unix_nano": 1688317271473734053,
                    "time_unix_nano": 1688317275250598013,
                    "value": 0
                  }
                ],
                "aggregation_temporality": 2,
                "is_monotonic": false
              }
            },
            {
              "name": "http.server.duration",
              "description": "measures the duration of the inbound HTTP request",
              "unit": "ms",
              "data": {
                "data_points": [
                  {
                    "attributes": {
                      "http.method": "GET",
                      "http.host": "localhost:4321",
                      "http.scheme": "http",
                      "http.flavor": "1.1",
                      "http.server_name": "0.0.0.0",
                      "net.host.port": 4321,
                      "http.status_code": 500
                    },
                    "start_time_unix_nano": 1688317271477757928,
                    "time_unix_nano": 1688317275250598013,
                    "count": 3,
                    "sum": 10,
                    "bucket_counts": [
                      0,
                      3,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0
                    ],
                    "explicit_bounds": [
                      0.0,
                      5.0,
                      10.0,
                      25.0,
                      50.0,
                      75.0,
                      100.0,
                      250.0,
                      500.0,
                      750.0,
                      1000.0,
                      2500.0,
                      5000.0,
                      7500.0,
                      10000.0
                    ],
                    "min": 2,
                    "max": 4
                  },
                  {
                    "attributes": {
                      "http.method": "GET",
                      "http.host": "localhost:4321",
                      "http.scheme": "http",
                      "http.flavor": "1.1",
                      "http.server_name": "0.0.0.0",
                      "net.host.port": 4321,
                      "http.status_code": 200
                    },
                    "start_time_unix_nano": 1688317271477757928,
                    "time_unix_nano": 1688317275250598013,
                    "count": 4,
                    "sum": 7,
                    "bucket_counts": [
                      0,
                      4,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0
                    ],
                    "explicit_bounds": [
                      0.0,
                      5.0,
                      10.0,
                      25.0,
                      50.0,
                      75.0,
                      100.0,
                      250.0,
                      500.0,
                      750.0,
                      1000.0,
                      2500.0,
                      5000.0,
                      7500.0,
                      10000.0
                    ],
                    "min": 1,
                    "max": 3
                  }
                ],
                "aggregation_temporality": 2
              }
            }
          ],
          "schema_url": ""
        }
      ],
      "schema_url": ""
    }
  ]
}
{
  "resource_metrics": [
    {
      "resource": {
        "attributes": {
          "telemetry.sdk.language": "python",
          "telemetry.sdk.name": "opentelemetry",
          "telemetry.sdk.version": "1.18.0",
          "service.name": "python-flask"
        },
        "schema_url": ""
      },
      "scope_metrics": [
        {
          "scope": {
            "name": "opentelemetry.instrumentation.flask",
            "version": "0.39b0",
            "schema_url": ""
          },
          "metrics": [
            {
              "name": "http.server.active_requests",
              "description": "measures the number of concurrent HTTP requests that are currently in-flight",
              "unit": "requests",
              "data": {
                "data_points": [
                  {
                    "attributes": {
                      "http.method": "GET",
                      "http.host": "localhost:4321",
                      "http.scheme": "http",
                      "http.flavor": "1.1",
                      "http.server_name": "0.0.0.0"
                    },
                    "start_time_unix_nano": 1688317271473734053,
                    "time_unix_nano": 1688317280243504501,
                    "value": 0
                  }
                ],
                "aggregation_temporality": 2,
                "is_monotonic": false
              }
            },
            {
              "name": "http.server.duration",
              "description": "measures the duration of the inbound HTTP request",
              "unit": "ms",
              "data": {
                "data_points": [],
                "aggregation_temporality": 2
              }
            }
          ],
          "schema_url": ""
        }
      ],
      "schema_url": ""
    }
  ]
}
```
</details>

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="lab-1.4-logs-instrumentation"></a>
## Lab 1.4 - Logs instrumentation

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with logs instrumentation: `git diff --no-index python-flask/1-bare python-flask/4-logs`

Questions to explore:

* What dependencies were added? Note: Python dependencies are declared in the [`requirements.txt`](python-flask/4-logs/requirements.txt) file.
* How did the code change in [`app.py`](python-flask/4-logs/app.py)?
* How did the environment variables change in [`Dockerfile`](python-flask/4-logs/Dockerfile)?
* How do these changes compare with the traces and metrics instrumentations?

Things to know:

* The app uses a `BatchLogRecordProcessor` for each exporter.
* The app uses a `ConsoleLogExporter` that serves the same purpose as the `ConsoleSpanExporter` from the traces instrumentation.

**Step 2.** Run the app: `APP=python-flask/4-logs docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal. Notice where the original log messages are stored, and the default metadata that is included in the logs.

<details>
<summary>View sample logs</summary>

```json
{
  "body": "\u001b[31m\u001b[1mWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\u001b[0m\n * Running on all addresses (0.0.0.0)\n * Running on http://127.0.0.1:4321\n * Running on http://172.27.0.2:4321",
  "severity_number": "<SeverityNumber.INFO: 9>",
  "severity_text": "INFO",
  "attributes": {},
  "timestamp": "2023-06-26T20:33:30.835571Z",
  "trace_id": "0x00000000000000000000000000000000",
  "span_id": "0x0000000000000000",
  "trace_flags": 0,
  "resource": "BoundedAttributes({'telemetry.sdk.language': 'python', 'telemetry.sdk.name': 'opentelemetry', 'telemetry.sdk.version': '1.18.0', 'service.name': 'python-flask'}, maxlen=None)"
}
{
  "body": "\u001b[33mPress CTRL+C to quit\u001b[0m",
  "severity_number": "<SeverityNumber.INFO: 9>",
  "severity_text": "INFO",
  "attributes": {},
  "timestamp": "2023-06-26T20:33:30.837132Z",
  "trace_id": "0x00000000000000000000000000000000",
  "span_id": "0x0000000000000000",
  "trace_flags": 0,
  "resource": "BoundedAttributes({'telemetry.sdk.language': 'python', 'telemetry.sdk.name': 'opentelemetry', 'telemetry.sdk.version': '1.18.0', 'service.name': 'python-flask'}, maxlen=None)"
}
{
  "body": "172.27.0.1 - - [26/Jun/2023 20:33:36] \"GET / HTTP/1.1\" 200 -",
  "severity_number": "<SeverityNumber.INFO: 9>",
  "severity_text": "INFO",
  "attributes": {},
  "timestamp": "2023-06-26T20:33:36.228817Z",
  "trace_id": "0x00000000000000000000000000000000",
  "span_id": "0x0000000000000000",
  "trace_flags": 0,
  "resource": "BoundedAttributes({'telemetry.sdk.language': 'python', 'telemetry.sdk.name': 'opentelemetry', 'telemetry.sdk.version': '1.18.0', 'service.name': 'python-flask'}, maxlen=None)"
}
{
  "body": "Exception on /error [GET]",
  "severity_number": "<SeverityNumber.ERROR: 17>",
  "severity_text": "ERROR",
  "attributes": {
    "exception.type": "ZeroDivisionError",
    "exception.message": "division by zero",
    "exception.stacktrace": "Traceback (most recent call last):\n  File \"/usr/local/lib/python3.10/site-packages/flask/app.py\", line 2190, in wsgi_app\n    response = self.full_dispatch_request()\n  File \"/usr/local/lib/python3.10/site-packages/flask/app.py\", line 1486, in full_dispatch_request\n    rv = self.handle_user_exception(e)\n  File \"/usr/local/lib/python3.10/site-packages/flask/app.py\", line 1484, in full_dispatch_request\n    rv = self.dispatch_request()\n  File \"/usr/local/lib/python3.10/site-packages/flask/app.py\", line 1469, in dispatch_request\n    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)\n  File \"//app.py\", line 50, in error\n    return eval('0/0')\n  File \"<string>\", line 1, in <module>\nZeroDivisionError: division by zero\n"
  },
  "timestamp": "2023-07-02T16:59:07.160477Z",
  "trace_id": "0x00000000000000000000000000000000",
  "span_id": "0x0000000000000000",
  "trace_flags": 1,
  "resource": "BoundedAttributes({'telemetry.sdk.language': 'python', 'telemetry.sdk.name': 'opentelemetry', 'telemetry.sdk.version': '1.18.0', 'service.name': 'python-flask'}, maxlen=None)"
}
```
</details>

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="lab-1.5-complete-instrumentation"></a>
## Lab 1.5 - Complete instrumentation

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with logs instrumentation: `git diff --no-index python-flask/1-bare python-flask/5-complete`

**Step 2.** Run the app: `APP=python-flask/5-complete docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal. Notice how the telemetry changes when the trace, metrics, and logs instrumentations are used together:

* The app is emitting additional metrics.
* Metrics do not include `trace_id` or `span_id` because they are aggregates.
* Only the logs within custom spans include `trace_id` and `span_id`. This is because the logger used by Flask writes logs outside of the context of traces ([source](https://github.com/open-telemetry/opentelemetry-python/issues/2455)).

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="lab-1.6-automatic-instrumentation-for-java"></a>
## Lab 1.6 - Automatic instrumentation for Java

Some languages can be instrumented with without modifying the application code. Java is one of those languages.


### Review the bare Java app

**Step 1.** Review the app code in a text editor:

* [`java-springboot/1-bare/src/main/java/com/grafana/otelworkshop/springboot/App.java`](java-springboot/1-bare/src/main/java/com/grafana/otelworkshop/springboot/App.java)
* [`java-springboot/1-bare/src/main/java/com/grafana/otelworkshop/springboot/AppController.java`](java-springboot/1-bare/src/main/java/com/grafana/otelworkshop/springboot/AppController.java)
* [`java-springboot/1-bare/src/main/java/com/grafana/otelworkshop/springboot/AppErrorController.java`](java-springboot/1-bare/src/main/java/com/grafana/otelworkshop/springboot/AppErrorController.java)

**Step 2.** Run the app: `APP=java-springboot/1-bare docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/) - Notice that the app responds with `ok` for any message.

**Step 4.** View the app logs in your terminal. Notice that the app writes logs when the app starts, and when the app handles a request in the web browser.

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


### Compare the Java app with automatic instrumentation

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with traces instrumentation: `git diff --no-index java-springboot/1-bare java-springboot/2-complete-auto`

**Step 2.** Run the app: `APP=java-springboot/1-bare docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal.

<details>
<summary>View sample trace logs</summary>

```sh
[otel.javaagent 2023-06-27 13:17:37:463 +0000] [http-nio-4321-exec-1] INFO io.opentelemetry.exporter.logging.LoggingSpanExporter - 'AppController.index' : d3572661fa424301e427d9135ba938bc e9eb751209030116 INTERNAL [tracer: io.opentelemetry.spring-webmvc-3.1:1.27.0-alpha] AttributesMap{data={thread.id=22, thread.name=http-nio-4321-exec-1}, capacity=128, totalAddedValues=2}
[otel.javaagent 2023-06-27 13:17:37:466 +0000] [http-nio-4321-exec-1] INFO io.opentelemetry.exporter.logging.LoggingSpanExporter - 'GET /' : d3572661fa424301e427d9135ba938bc 8baa428d9ff7d08e SERVER [tracer: io.opentelemetry.tomcat-7.0:1.27.0-alpha] AttributesMap{data={thread.id=22, net.protocol.name=http, net.sock.peer.port=64236, http.method=GET, http.scheme=http, net.protocol.version=1.1, net.host.port=4321, http.response_content_length=2, net.sock.host.addr=172.28.0.2, http.status_code=200, http.route=/, thread.name=http-nio-4321-exec-1, user_agent.original=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36, net.host.name=localhost, http.target=/, net.sock.peer.addr=172.28.0.1}, capacity=128, totalAddedValues=16}
```
</details>

<details>
<summary>View sample metric logs</summary>

```sh
[otel.javaagent 2023-06-27 13:18:15:214 +0000] [PeriodicMetricReader-1] INFO io.opentelemetry.exporter.logging.LoggingMetricExporter - Received a collection of 19 metrics for export.
[otel.javaagent 2023-06-27 13:18:15:215 +0000] [PeriodicMetricReader-1] INFO io.opentelemetry.exporter.logging.LoggingMetricExporter - metric: ImmutableMetricData{resource=Resource{schemaUrl=https://opentelemetry.io/schemas/1.20.0, attributes={container.id="a8957f6746758bcb57b91ed77064a437fd8cf24e15fe705318fb7bef246580cd", host.arch="aarch64", host.name="a8957f674675", os.description="Linux 5.10.76-linuxkit", os.type="linux", process.command_args=[/opt/java/openjdk/bin/java, -jar, /data/app-0.1.0.jar, --server.port=4321], process.executable.path="/opt/java/openjdk/bin/java", process.pid=8, process.runtime.description="Eclipse Adoptium OpenJDK 64-Bit Server VM 11.0.19+7", process.runtime.name="OpenJDK Runtime Environment", process.runtime.version="11.0.19+7", service.name="java-springboot", telemetry.auto.version="1.27.0", telemetry.sdk.language="java", telemetry.sdk.name="opentelemetry", telemetry.sdk.version="1.27.0"}}, instrumentationScopeInfo=InstrumentationScopeInfo{name=io.opentelemetry.runtime-telemetry-java8, version=1.27.0-alpha, schemaUrl=null, attributes={}}, name=process.runtime.jvm.memory.committed, description=Measure of memory committed, unit=By, type=LONG_SUM, data=ImmutableSumData{points=[ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="CodeHeap 'non-nmethods'", type="non_heap"}, value=2555904, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="CodeHeap 'non-profiled nmethods'", type="non_heap"}, value=4587520, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="Compressed Class Space", type="non_heap"}, value=6762496, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="G1 Eden Space", type="heap"}, value=88080384, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="CodeHeap 'profiled nmethods'", type="non_heap"}, value=16842752, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="Metaspace", type="non_heap"}, value=47919104, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="G1 Old Gen", type="heap"}, value=71303168, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="G1 Survivor Space", type="heap"}, value=10485760, exemplars=[]}], monotonic=false, aggregationTemporality=CUMULATIVE}}
[otel.javaagent 2023-06-27 13:18:15:215 +0000] [PeriodicMetricReader-1] INFO io.opentelemetry.exporter.logging.LoggingMetricExporter - metric: ImmutableMetricData{resource=Resource{schemaUrl=https://opentelemetry.io/schemas/1.20.0, attributes={container.id="a8957f6746758bcb57b91ed77064a437fd8cf24e15fe705318fb7bef246580cd", host.arch="aarch64", host.name="a8957f674675", os.description="Linux 5.10.76-linuxkit", os.type="linux", process.command_args=[/opt/java/openjdk/bin/java, -jar, /data/app-0.1.0.jar, --server.port=4321], process.executable.path="/opt/java/openjdk/bin/java", process.pid=8, process.runtime.description="Eclipse Adoptium OpenJDK 64-Bit Server VM 11.0.19+7", process.runtime.name="OpenJDK Runtime Environment", process.runtime.version="11.0.19+7", service.name="java-springboot", telemetry.auto.version="1.27.0", telemetry.sdk.language="java", telemetry.sdk.name="opentelemetry", telemetry.sdk.version="1.27.0"}}, instrumentationScopeInfo=InstrumentationScopeInfo{name=io.opentelemetry.runtime-telemetry-java8, version=1.27.0-alpha, schemaUrl=null, attributes={}}, name=process.runtime.jvm.buffer.limit, description=Total capacity of the buffers in this pool, unit=By, type=LONG_SUM, data=ImmutableSumData{points=[ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="direct"}, value=16384, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="mapped"}, value=0, exemplars=[]}], monotonic=false, aggregationTemporality=CUMULATIVE}}
[otel.javaagent 2023-06-27 13:18:15:216 +0000] [PeriodicMetricReader-1] INFO io.opentelemetry.exporter.logging.LoggingMetricExporter - metric: ImmutableMetricData{resource=Resource{schemaUrl=https://opentelemetry.io/schemas/1.20.0, attributes={container.id="a8957f6746758bcb57b91ed77064a437fd8cf24e15fe705318fb7bef246580cd", host.arch="aarch64", host.name="a8957f674675", os.description="Linux 5.10.76-linuxkit", os.type="linux", process.command_args=[/opt/java/openjdk/bin/java, -jar, /data/app-0.1.0.jar, --server.port=4321], process.executable.path="/opt/java/openjdk/bin/java", process.pid=8, process.runtime.description="Eclipse Adoptium OpenJDK 64-Bit Server VM 11.0.19+7", process.runtime.name="OpenJDK Runtime Environment", process.runtime.version="11.0.19+7", service.name="java-springboot", telemetry.auto.version="1.27.0", telemetry.sdk.language="java", telemetry.sdk.name="opentelemetry", telemetry.sdk.version="1.27.0"}}, instrumentationScopeInfo=InstrumentationScopeInfo{name=io.opentelemetry.runtime-telemetry-java8, version=1.27.0-alpha, schemaUrl=null, attributes={}}, name=process.runtime.jvm.buffer.count, description=The number of buffers in the pool, unit={buffers}, type=LONG_SUM, data=ImmutableSumData{points=[ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="direct"}, value=2, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="mapped"}, value=0, exemplars=[]}], monotonic=false, aggregationTemporality=CUMULATIVE}}
[otel.javaagent 2023-06-27 13:18:15:216 +0000] [PeriodicMetricReader-1] INFO io.opentelemetry.exporter.logging.LoggingMetricExporter - metric: ImmutableMetricData{resource=Resource{schemaUrl=https://opentelemetry.io/schemas/1.20.0, attributes={container.id="a8957f6746758bcb57b91ed77064a437fd8cf24e15fe705318fb7bef246580cd", host.arch="aarch64", host.name="a8957f674675", os.description="Linux 5.10.76-linuxkit", os.type="linux", process.command_args=[/opt/java/openjdk/bin/java, -jar, /data/app-0.1.0.jar, --server.port=4321], process.executable.path="/opt/java/openjdk/bin/java", process.pid=8, process.runtime.description="Eclipse Adoptium OpenJDK 64-Bit Server VM 11.0.19+7", process.runtime.name="OpenJDK Runtime Environment", process.runtime.version="11.0.19+7", service.name="java-springboot", telemetry.auto.version="1.27.0", telemetry.sdk.language="java", telemetry.sdk.name="opentelemetry", telemetry.sdk.version="1.27.0"}}, instrumentationScopeInfo=InstrumentationScopeInfo{name=io.opentelemetry.runtime-telemetry-java8, version=1.27.0-alpha, schemaUrl=null, attributes={}}, name=process.runtime.jvm.memory.limit, description=Measure of max obtainable memory, unit=By, type=LONG_SUM, data=ImmutableSumData{points=[ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="CodeHeap 'non-nmethods'", type="non_heap"}, value=5832704, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="CodeHeap 'non-profiled nmethods'", type="non_heap"}, value=122912768, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="Compressed Class Space", type="non_heap"}, value=1073741824, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="CodeHeap 'profiled nmethods'", type="non_heap"}, value=122912768, exemplars=[]}, ImmutableLongPointData{startEpochNanos=1687871835177876000, epochNanos=1687871895178245000, attributes={pool="G1 Old Gen", type="heap"}, value=2084569088, exemplars=[]}], monotonic=false, aggregationTemporality=CUMULATIVE}}
```
</details>

**Step 5.** Stop the app using Ctrl+C or ⌘-C.

Questions to explore:

* What files changed?
* How did [`Dockerfile`](java-springboot/2-complete-auto/Dockerfile) change?
* How does the telemetry data in Java compare to Python?


<a name="retrospective"></a>
## Retrospective

* What patterns and differences did you notice in the implementations across programming languages?
* What patterns and differences did you notice in the implementations of metrics, logs, and traces?
* How would you simplify the instrumentation for capturing telemetry for errors and exceptions in a complex application?
* How would you simplify the instrumentation of apps that span many files or levels of abstraction?
* How would you simplify the configuration of instrumentations for many deployed apps?
