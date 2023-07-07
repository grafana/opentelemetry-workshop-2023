# Lab 1. Instrumentation

## Contents

* [Preface](#preface)
* [1.1 - No instrumentation](#1.1-no-instrumentation)
* [1.2 - Traces instrumentation](#1.2-traces-instrumentation)
  * [1.2.1 - Custom spans](#1.2.1-custom-spans)
  * [1.2.2 - Distributed traces](#1.2.2-distributed-traces)
* [1.3 - Metrics instrumentation](#1.3-metrics-instrumentation)
  * [1.3.1 - Custom metrics](#1.3.1-custom-metrics)
* [1.4 - Logs instrumentation](#1.4-logs-instrumentation)
* [1.5 - Complete instrumentation](#1.5-complete-instrumentation)
* [1.6 - Automatic instrumentation for Java](#1.6-automatic-instrumentation-for-java)
* [1.7 - Resource attributes](#1.7-resource-attributes)
* [Retrospective](#retrospective)


<a name="preface"></a>
## Preface

Lab 1 introduces the fundamentals of [instrumentation](https://opentelemetry.io/docs/instrumentation/) with OpenTelemetry.

You will see how to instrument traces, metrics, and logs with a clear and systematic set of instructions. Lab 1 does not ship data to external destinations – that is covered in [Lab 2](../lab-2-collection). You will see the data in your terminal in Lab 1.

The lab uses an app implemented in two programming languages and app frameworks:

* **Python** using the [Flask](https://flask.palletsprojects.com/en/2.3.x/) framework ([`python-flask`](python-flask))
* **Java** using the [Spring Boot](https://spring.io/projects/spring-boot) framework ([`java-springboot`](java-springboot))

There are instrumentation-specific variants of the app:

* **Bare** - No instrumentation
* **Traces** - Traces instrumentation
* **Metrics** - Metrics instrumentation
* **Logs** - Logs instrumentation
* **Complete** - All three instrumentations with correlations

This lab requires you to run commands in the terminal. You will need to navigate into the `lab-1-instrumentation` directory and run the commands from there.

Using the `git diff` command, you can compare a **bare** app with one of its instrumentation variants. This lets you see exactly what steps were needed to instrument traces, metrics, or logs. Nothing more, nothing less.

Example:

```sh
git diff --no-index python-flask/bare python-flask/traces
```

To run one of the apps, navigate to `lab-1-instrumentation` and run the command below after changing the value of `path_to_app_directory`:

```sh
APP=path_to_app_directory docker-compose up --build
```

Example:

```sh
APP=python-flask/complete docker-compose up --build
```

This command builds and runs the app on port `4321`. You can view the running app in your web browser at [http://localhost:4321/](http://localhost:4321/) and then view the activity in your terminal.

You can control the app using these endpoints:

* [http://localhost:4321/](http://localhost:4321/) - Responds with `ok`
* [http://localhost:4321/error](http://localhost:4321/error) - Responds with an error message after attempting to divide by zero

<a name="1.1-no-instrumentation"></a>
## 1.1 - No instrumentation

Before instrumenting the app, let's see how it behaves on its own. This will help us understand the effect of each instrumentation in the next sections of the lab.

**Step 1.** Review the app code in a text editor:

* [`python-flask/bare/app.py`](python-flask/bare/app.py) - The application code.
* [`python-flask/bare/requirements.txt`](python-flask/bare/requirements.txt) - The dependencies for the app.
* [`python-flask/bare/Dockerfile`](python-flask/bare/Dockerfile) - Builds the app as a container.

**Step 2.** Run the app: `APP=python-flask/bare docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/) - Notice that the app responds with `ok` for any message.

**Step 4.** View the app logs in your terminal. Notice that the app writes logs when the app starts, and when the app handles a request in the web browser.

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="1.2-traces-instrumentation"></a>
## 1.2 - Traces instrumentation

Traces provide visibility into the execution of one or more applications or services. A **trace** is a set of one or more **spans** that represent individual units of work (the spans) within a broader, single transaction of work (the trace).

Traces include the following data:

* [**Context**](https://opentelemetry.io/docs/concepts/signals/traces/#span-context) - Metadata about the trace in which the span participates, such as `TraceID` and `SpanId`.
* [**Attributes**](https://opentelemetry.io/docs/concepts/signals/traces/#attributes) - Metadata about the current span. Attributes are arbitrary key-value pairs that should conform to [semantic conventions](https://opentelemetry.io/docs/specs/otel/trace/semantic_conventions/). Instrumentation libraries automatically add some attributes to each span.
* [**Events**](https://opentelemetry.io/docs/concepts/signals/traces/#span-events) - Indicates a notable event in the trace, serving the purpose of a log or annotation.
* [**Links**](https://opentelemetry.io/docs/concepts/signals/traces/#span-links) - Establishes links between spans. These are useful for linking traces with asynchronous spans, such as when using message queues. Links are not necessary for most traces which are synchronous.
* [**Status**](https://opentelemetry.io/docs/concepts/signals/traces/#span-status) - Indicates the success or failure of a span, if applicable. Values can be `Ok`, `Error`, or `Unset`. Instrumentation libraries automatically set the value to `Error` when handling exceptions, but they do not automatically set the value based on the HTTP status code. The default value is `Unset`.
* [**Kind**](https://opentelemetry.io/docs/concepts/signals/traces/#span-kind) - Indicates the source of a span. Values can be `Client`, `Server`, `Internal`, `Producer`, or `Consumer`. Instrumentation libraries automatically set the value to `Server` for a parent span, and `Internal` for child spans.

Let's see an example in action.

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with traces instrumentation: `git diff --no-index python-flask/bare python-flask/traces`

Questions to explore:

* What dependencies were added? Note: Python dependencies are declared in the [`requirements.txt`](python-flask/traces/requirements.txt) file.
* How did the code change in [`app.py`](python-flask/traces/app.py)?
* How did the environment variables change in [`Dockerfile`](python-flask/traces/Dockerfile)?

Things to know:

* The app uses a `BatchSpanProcessor` for each exporter.
* The app uses a `ConsoleSpanExporter` to send spans to the terminal (i.e. `stdout`).
* The app uses `FlaskInstrumentor` to auto-instrument the web app framework.

Best practices:

* `ConsoleSpanExporter` is a great tool when implementing instrumentations in development, because it rules out any variables downstream of the app (e.g. networking issues or database issues) when troubleshooting your implementation. In production, you can omit `ConsoleSpanExporter` to prevent noisy logs.

**Step 2.** Run the app: `APP=python-flask/traces docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal. Notice that the traces appear in the terminal.

<details>
<summary><b style='color:#2f81f7'>Click to view a sample trace 🔎</b></summary>

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

**Step 5.** Open the `/error` endpoint in a web browser: [http://localhost:4321/error](http://localhost:4321/error)

**Step 6.** This caused an error in the app. View the app logs in your terminal to see how errors appear in traces.

<details>
<summary><b style='color:#2f81f7'>Click to view a sample trace 🔎</b></summary>

```json
{
  "name": "/error",
  "context": {
    "trace_id": "0xdcbf6bb7013f56929d82de85ca552aa7",
    "span_id": "0xc894470b684e6a91",
    "trace_state": "[]"
  },
  "kind": "SpanKind.SERVER",
  "parent_id": null,
  "start_time": "2023-07-07T20:21:54.662432Z",
  "end_time": "2023-07-07T20:21:54.681124Z",
  "status": {
    "status_code": "ERROR",
    "description": "ZeroDivisionError: division by zero"
  },
  "attributes": {
    "http.method": "GET",
    "http.server_name": "0.0.0.0",
    "http.scheme": "http",
    "net.host.port": 4321,
    "http.host": "localhost:4321",
    "http.target": "/error",
    "net.peer.ip": "172.25.0.1",
    "http.user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "net.peer.port": 64470,
    "http.flavor": "1.1",
    "http.route": "/error",
    "http.status_code": 500
  },
  "events": [
    {
      "name": "exception",
      "timestamp": "2023-07-07T20:21:54.681109Z",
      "attributes": {
        "exception.type": "ZeroDivisionError",
        "exception.message": "division by zero",
        "exception.stacktrace": "Traceback (most recent call last):\n  File \"/usr/local/lib/python3.10/site-packages/opentelemetry/trace/__init__.py\", line 573, in use_span\n  yield span\n  File \"/usr/local/lib/python3.10/site-packages/flask/app.py\", line 2190, in wsgi_app\n  response = self.full_dispatch_request()\n  File \"/usr/local/lib/python3.10/site-packages/flask/app.py\", line 1486, in full_dispatch_request\n  rv = self.handle_user_exception(e)\n  File \"/usr/local/lib/python3.10/site-packages/flask/app.py\", line 1484, in full_dispatch_request\n  rv = self.dispatch_request()\n  File \"/usr/local/lib/python3.10/site-packages/flask/app.py\", line 1469, in dispatch_request\n  return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)\n  File \"//app.py\", line 25, in error\n  return eval('0/0')\n  File \"<string>\", line 1, in <module>\nZeroDivisionError: division by zero\n",
        "exception.escaped": "False"
      }
    }
  ],
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

**Step 7.** Stop the app using Ctrl+C or ⌘-C.


<a name="1.2.1-custom-spans"></a>
### 1.2.1 - Custom spans

You can add or modify spans in a trace. Let's see some examples in action.

**Step 1.** Compare the code of the app with default traces instrumentation to the code of the app with the additional custom instrumentation: `git diff --no-index python-flask/traces python-flask/traces-custom`

**Step 2.** Run the app: `APP=python-flask/traces-custom docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal.

<details>
<summary><b style='color:#2f81f7'>Click to view a sample trace 🔎</b></summary>

```json
{
  "name": "child_span_2",
  "context": {
    "trace_id": "0xc63d5fae79c8a6b6bd93f6fd0ec65658",
    "span_id": "0xe1bbe20caae47656",
    "trace_state": "[]"
  },
  "kind": "SpanKind.INTERNAL",
  "parent_id": "0x698722f5acdaece7",
  "start_time": "2023-07-03T16:45:29.657311Z",
  "end_time": "2023-07-03T16:45:29.657325Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {
    "greeting": "hello!"
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
{
  "name": "child_span_1",
  "context": {
    "trace_id": "0xc63d5fae79c8a6b6bd93f6fd0ec65658",
    "span_id": "0x698722f5acdaece7",
    "trace_state": "[]"
  },
  "kind": "SpanKind.INTERNAL",
  "parent_id": "0xa1a780b9ece706c7",
  "start_time": "2023-07-03T16:45:29.657285Z",
  "end_time": "2023-07-03T16:45:29.657344Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {},
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
{
  "name": "/",
  "context": {
    "trace_id": "0xc63d5fae79c8a6b6bd93f6fd0ec65658",
    "span_id": "0xa1a780b9ece706c7",
    "trace_state": "[]"
  },
  "kind": "SpanKind.SERVER",
  "parent_id": null,
  "start_time": "2023-07-03T16:45:29.653985Z",
  "end_time": "2023-07-03T16:45:29.657530Z",
  "status": {
    "status_code": "OK"
  },
  "attributes": {
    "http.method": "GET",
    "http.server_name": "0.0.0.0",
    "http.scheme": "http",
    "net.host.port": 4321,
    "http.host": "localhost:4321",
    "http.target": "/",
    "net.peer.ip": "172.25.0.1",
    "http.user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "net.peer.port": 59842,
    "http.flavor": "1.1",
    "http.route": "/",
    "http.status_code": 200
  },
  "events": [
    {
      "name": "we made a friend",
      "timestamp": "2023-07-03T16:45:29.657357Z",
      "attributes": {
        "mood": "happy"
      }
    }
  ],
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

Each trace now has three spans instead of one. We modified the instrumentation to include two custom child spans for each trace. The logs display the spans in reverse order, so the parent span will be the last span in your terminal output.

Here's what we modified and how that appears in the trace data:

* **Attributes** - We added a custom attribute named `greeting` with a value of `hello!` to one of our child spans.
* **Events** - We added a custom event to the parent span. We named the event `we made a friend` and gave it a custom attribute named `mood` with a value of `happy`.
* **Status** - We set the value of parent span status (`status_code`) to `OK` to indicate success.

It's also worth noting:

* **Context** - The trace context for each span includes the same TraceId (`trace_id`). This was handled by the instrumentation library.

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="1.2.2-distributed-traces"></a>
### 1.2.2 - Distributed traces

A **distributed trace** has spans from two or more instrumented apps. This is achieved with [context propagation](https://opentelemetry.io/docs/concepts/signals/traces/#context-propagation). When an instrumented app talks to another app, it shares (or "propagates") its trace context (e.g. `TraceId`) using an HTTP header called [`traceparent`](https://www.w3.org/TR/trace-context/#traceparent-header). If the second app is also instrumented, it will look for that header, apply the context to its spans, and propagate the context to any apps that it talks with. Instrumentation libraries automatically handle context propagation. Once you instrument your apps, you don't need to do anything else to get them to share their contexts with each other. Easy!

Let's see this in action. We can create a distributed trace from a single app by instructing the app send a request to itself over the network.

**Step 1.** Compare the code of the app with default traces instrumentation to the code of the app with the additional custom instrumentation: `git diff --no-index python-flask/traces python-flask/traces-distributed`

Questions to explore:

* Where does context propogation occur in the code?

**Step 2.** Run the app: `APP=python-flask/traces-distributed docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal. Whenever you visit the app in your web browser, a distributed trace with three spans is produced. The spans are logged in reverse order in your terminal output, meaning the root span is the last span to appear in the output.

<details>
<summary><b style='color:#2f81f7'>Click to view a sample trace 🔎</b></summary>

```json
{
  "name": "/test",
  "context": {
    "trace_id": "0x24a21d29f7b3aba22bc8fdcccc4fd0bd",
    "span_id": "0x8ff0d623a6ddfca8",
    "trace_state": "[]"
  },
  "kind": "SpanKind.SERVER",
  "parent_id": "0xc42e73e0af1e038a",
  "start_time": "2023-07-03T19:04:40.769832Z",
  "end_time": "2023-07-03T19:04:40.770421Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {
    "http.method": "GET",
    "http.server_name": "0.0.0.0",
    "http.scheme": "http",
    "net.host.port": 4321,
    "http.host": "localhost:4321",
    "http.target": "/test",
    "net.peer.ip": "127.0.0.1",
    "http.user_agent": "python-requests/2.31.0",
    "net.peer.port": 53092,
    "http.flavor": "1.1",
    "http.route": "/test",
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
{
  "name": "HTTP GET",
  "context": {
    "trace_id": "0x24a21d29f7b3aba22bc8fdcccc4fd0bd",
    "span_id": "0xc42e73e0af1e038a",
    "trace_state": "[]"
  },
  "kind": "SpanKind.CLIENT",
  "parent_id": "0x0764d117c3916e7d",
  "start_time": "2023-07-03T19:04:40.767925Z",
  "end_time": "2023-07-03T19:04:40.772192Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {
    "http.method": "GET",
    "http.url": "http://localhost:4321/test",
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
{
  "name": "/",
  "context": {
    "trace_id": "0x24a21d29f7b3aba22bc8fdcccc4fd0bd",
    "span_id": "0x0764d117c3916e7d",
    "trace_state": "[]"
  },
  "kind": "SpanKind.SERVER",
  "parent_id": null,
  "start_time": "2023-07-03T19:04:40.746530Z",
  "end_time": "2023-07-03T19:04:40.772403Z",
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
    "net.peer.ip": "172.25.0.1",
    "http.user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "net.peer.port": 60346,
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

Here's an explanation of the spans in the sample above. Remember that the spans are displayed in reverse order in your terminal output.

*Span 1* - This root span was recorded by the app when it received your request to the `/` endpoint in your web browser.

* `context` shows a `trace_id` of `0x24a21d29f7b3aba22bc8fdcccc4fd0bd` and a `span_id` of `0xc42e73e0af1e038a`.
* `parent_id` is set to `null` because it is the root span.
* `kind` is set to `SpanKind.SERVER`, because it represents the span of a request *received* by the app.
* The `http.user_agent` attribute shows how your web browser described itself to the app.
  
*Span 2* - This span was recorded by the app when it *sent* the request for the `/test` endpoint.

* `context` shows a `trace_id` of `0x24a21d29f7b3aba22bc8fdcccc4fd0bd`, which was obtained from the `traceparent` header that the parent app shared in its request.
* `parent_id` is set to `0xc42e73e0af1e038a`, which was obtained from the `traceparent` header that the parent app shared in its request.
* `kind` is set to `SpanKind.CLIENT`, because it represents the span of a request *sent* by the app.
  
*Span 3* - This span was recorded by the app when it *received* the request for the `/test` endpoint.

* `context` shows a `trace_id` of `0x24a21d29f7b3aba22bc8fdcccc4fd0bd`, which was obtained from the `traceparent` header that the parent app shared in its request.
* `parent_id` is set to `0xc42e73e0af1e038a`, which was obtained from the `traceparent` header that the parent app shared in its request.
* `kind` is set to `SpanKind.SERVER`, because it represents the span of a request *received* by the app.
* The `http.user_agent` attribute is set to `python-requests/2.31.0`, which was the client library that the app used to send a request to the `/test` endpoint.

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="1.3-metrics-instrumentation"></a>
## 1.3 - Metrics instrumentation

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with metrics instrumentation: `git diff --no-index python-flask/bare python-flask/metrics`

Questions to explore:

* What dependencies were added? Note: Python dependencies are declared in the [`requirements.txt`](python-flask/metrics/requirements.txt) file.
* How did the code change in [`app.py`](python-flask/metrics/app.py)?
* How did the environment variables change in [`Dockerfile`](python-flask/metrics/app.py)?
* How do these changes compare with the traces instrumentation?

Things to know:

* The app uses a `PeriodicExportingMetricReader` for each exporter. Notice the configurable export interval that is set to `5000ms`.
* The app uses a `ConsoleMetricExporter` that serves the same purpose as the `ConsoleSpanExporter` from the traces instrumentation.

**Step 2.** Run the app: `APP=python-flask/metrics docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal. Notice that the metrics appear in the terminal every 5 seconds, as instructed by the `5000ms` export interval.

<details>
<summary><b style='color:#2f81f7'>Click to view sample metrics 🔎</b></summary>

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


<a name="1.3.1-custom-metrics"></a>
### 1.3.1 - Custom metrics

You can instrument custom metrics (or "meters") and add custom attributes to those metrics. Let's see some examples in action.

**Step 1.** Compare the code of the app with default metrics instrumentation to the code of the app with the additional custom instrumentation: `git diff --no-index python-flask/metrics python-flask/metrics-custom`

**Step 2.** Run the app: `APP=python-flask/metrics-custom docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal.

<details>
<summary><b style='color:#2f81f7'>Click to view sample metrics 🔎</b></summary>

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
                    "start_time_unix_nano": 1688409038744220923,
                    "time_unix_nano": 1688409042977454050,
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
                      "http.status_code": 200
                    },
                    "start_time_unix_nano": 1688409038745744548,
                    "time_unix_nano": 1688409042977454050,
                    "count": 6,
                    "sum": 10,
                    "bucket_counts": [
                      0,
                      6,
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
                    "max": 2
                  }
                ],
                "aggregation_temporality": 2
              }
            }
          ],
          "schema_url": ""
        },
        {
          "scope": {
            "name": "custom_meter",
            "version": null,
            "schema_url": ""
          },
          "metrics": [
            {
              "name": "custom_counter",
              "description": "",
              "unit": "",
              "data": {
                "data_points": [
                  {
                    "attributes": {
                      "foo": "bar"
                    },
                    "start_time_unix_nano": 1688409038745295798,
                    "time_unix_nano": 1688409042977454050,
                    "value": 6
                  }
                ],
                "aggregation_temporality": 2,
                "is_monotonic": true
              }
            },
            {
              "name": "custom_histogram",
              "description": "",
              "unit": "",
              "data": {
                "data_points": [
                  {
                    "attributes": {
                      "foo": "baz"
                    },
                    "start_time_unix_nano": 1688409038745339965,
                    "time_unix_nano": 1688409042977454050,
                    "count": 6,
                    "sum": 26972,
                    "bucket_counts": [
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      0,
                      0,
                      1,
                      1,
                      2,
                      1,
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
                    "min": 334,
                    "max": 8166
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
```
</details>

Notice the following:

* We created a `custom_counter` meter and incremented it by 1 for each page load.
* We created a `custom_histogram` meter and recorded a random number for each page load.
* We set a custom attribute named `foo` with a value of either `bar` or `baz` each time we invoked one of the meters.

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="1.4-logs-instrumentation"></a>
## 1.4 - Logs instrumentation

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with logs instrumentation: `git diff --no-index python-flask/bare python-flask/logs`

Questions to explore:

* What dependencies were added? Note: Python dependencies are declared in the [`requirements.txt`](python-flask/logs/requirements.txt) file.
* How did the code change in [`app.py`](python-flask/logs/app.py)?
* How did the environment variables change in [`Dockerfile`](python-flask/logs/Dockerfile)?
* How do these changes compare with the traces and metrics instrumentations?

Things to know:

* The app uses a `BatchLogRecordProcessor` for each exporter.
* The app uses a `ConsoleLogExporter` that serves the same purpose as the `ConsoleSpanExporter` from the traces instrumentation.

**Step 2.** Run the app: `APP=python-flask/logs docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal. Notice where the original log messages are stored, and the default metadata that is included in the logs.

<details>
<summary><b style='color:#2f81f7'>Click to view sample logs 🔎</b></summary>

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


<a name="1.5-complete-instrumentation"></a>
## 1.5 - Complete instrumentation

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with logs instrumentation: `git diff --no-index python-flask/bare python-flask/complete`

**Step 2.** Run the app: `APP=python-flask/complete docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal. Notice how the telemetry changes when the trace, metrics, and logs instrumentations are used together:

* The app is emitting additional metrics.
* Metrics do not include `trace_id` or `span_id` because they are aggregates.
* Only the logs within custom spans include `trace_id` and `span_id`. This is because the logger used by Flask writes logs outside of the context of traces ([source](https://github.com/open-telemetry/opentelemetry-python/issues/2455)).

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


<a name="1.6-automatic-instrumentation-for-java"></a>
## 1.6 - Automatic instrumentation for Java

Some languages can be instrumented with without modifying the application code. Java is one of those languages.


### Review the bare Java app

**Step 1.** Review the app code in a text editor:

* [`java-springboot/bare/src/main/java/com/grafana/otelworkshop/springboot/App.java`](java-springboot/bare/src/main/java/com/grafana/otelworkshop/springboot/App.java)
* [`java-springboot/bare/src/main/java/com/grafana/otelworkshop/springboot/AppController.java`](java-springboot/bare/src/main/java/com/grafana/otelworkshop/springboot/AppController.java)
* [`java-springboot/bare/src/main/java/com/grafana/otelworkshop/springboot/AppErrorController.java`](java-springboot/bare/src/main/java/com/grafana/otelworkshop/springboot/AppErrorController.java)

**Step 2.** Run the app: `APP=java-springboot/bare docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/) - Notice that the app responds with `ok` for any message.

**Step 4.** View the app logs in your terminal. Notice that the app writes logs when the app starts, and when the app handles a request in the web browser.

**Step 5.** Stop the app using Ctrl+C or ⌘-C.


### Compare the Java app with automatic instrumentation

**Step 1.** Compare the code of the app with no instrumentation to the code of the app with traces instrumentation: `git diff --no-index java-springboot/bare java-springboot/complete-auto`

**Step 2.** Run the app: `APP=java-springboot/complete-auto docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal.

<details>
<summary><b style='color:#2f81f7'>Click to view a sample trace 🔎</b></summary>

```sh
[otel.javaagent 2023-06-27 13:17:37:463 +0000] [http-nio-4321-exec-1] INFO io.opentelemetry.exporter.logging.LoggingSpanExporter - 'AppController.index' : d3572661fa424301e427d9135ba938bc e9eb751209030116 INTERNAL [tracer: io.opentelemetry.spring-webmvc-3.1:1.27.0-alpha] AttributesMap{data={thread.id=22, thread.name=http-nio-4321-exec-1}, capacity=128, totalAddedValues=2}
[otel.javaagent 2023-06-27 13:17:37:466 +0000] [http-nio-4321-exec-1] INFO io.opentelemetry.exporter.logging.LoggingSpanExporter - 'GET /' : d3572661fa424301e427d9135ba938bc 8baa428d9ff7d08e SERVER [tracer: io.opentelemetry.tomcat-7.0:1.27.0-alpha] AttributesMap{data={thread.id=22, net.protocol.name=http, net.sock.peer.port=64236, http.method=GET, http.scheme=http, net.protocol.version=1.1, net.host.port=4321, http.response_content_length=2, net.sock.host.addr=172.28.0.2, http.status_code=200, http.route=/, thread.name=http-nio-4321-exec-1, user_agent.original=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36, net.host.name=localhost, http.target=/, net.sock.peer.addr=172.28.0.1}, capacity=128, totalAddedValues=16}
```
</details>

<details>
<summary><b style='color:#2f81f7'>Click to view sample metrics 🔎</b></summary>

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
* How did [`Dockerfile`](java-springboot/complete-auto/Dockerfile) change?
* How does the telemetry data in Java compare to Python?


<a name="1.7-resource-attributes"></a>
## 1.7 - Resource attributes

[Resource attributes](https://opentelemetry.io/docs/instrumentation/js/resources/) describe the instrumented entity. Instrumentation libraries will automatically detect certain resource attributes and include them in the telemetry payloads. Below is an example of the resource attributes that were automatically created by the instrumentation libraries in [Section 1.5](#1.5-complete-instrumentation).

<details>
<summary><b style='color:#2f81f7'>Click to view resource attributes 🔎</b></summary>

```json
{
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.18.0",
      "service.name": "python-flask"
    }
  }
}
```
</details>

Let's change these resource attributes. We'll use [environment variables](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/) to configure the resource attributes. This approach has two benefits: you don't need to change the application code, and you can apply it to any programming language.

**Step 1.** Open the [`env`](env) file in a text editor. Remove the `#` character from the start of each line. Save the file, then close the text editor.

The file now looks like this:

```sh
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=workshop,service.version=1.0.1,greeting=Hello World!
OTEL_SERVICE_NAME=myservice
```

**Step 2.** Run the app: `APP=python-flask/complete docker-compose up --build`

**Step 3.** Open the app in a web browser: [http://localhost:4321/](http://localhost:4321/)

**Step 4.** View the app logs in your terminal. Look for the resource attributes included in the metrics.

<details>
<summary><b style='color:#2f81f7'>Click to view resource attributes 🔎</b></summary>

```json
{
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.18.0",
      "deployment.environment": "workshop",
      "greeting": "Hello World!",
      "service.version": "1.0.1",
      "service.name": "myservice"
    }
  }
}
```
</details>

Notice the following changes:

* [`service.name`](https://opentelemetry.io/docs/specs/otel/resource/semantic_conventions/#service) is a standard resource attribute. The original value was `python-flask` as declared in the [Dockerfile](python-flask/complete/Dockerfile) of the app. This value was overridden to be `myservice` by the [`OTEL_SERVICE_NAME`](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_service_name) environment variable in the [`env`](env) file.
* [`service.version`](https://opentelemetry.io/docs/specs/otel/resource/semantic_conventions/#service) is a standard resource attribute. It was set by the [`OTEL_RESOURCE_ATTRIBUTES`](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes) environment variable in the [`env`](env) file.
* [`deployment.environment`](https://opentelemetry.io/docs/specs/otel/resource/semantic_conventions/deployment_environment/) is a standard resource attribute. It was set by the [`OTEL_RESOURCE_ATTRIBUTES`](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes) environment variable in the [`env`](env) file.
* `greeting` is a custom resource attribute. It was set by the [`OTEL_RESOURCE_ATTRIBUTES`](https://opentelemetry.io/docs/concepts/sdk-configuration/general-sdk-configuration/#otel_resource_attributes) environment variable in the [`env`](env) file.


<a name="retrospective"></a>
## Retrospective

* What patterns and differences did you notice in the implementations across programming languages?
* What patterns and differences did you notice in the implementations of metrics, logs, and traces?
* How would you simplify the instrumentation for capturing telemetry for errors and exceptions in a complex application?
* How would you simplify the instrumentation of apps that span many files or levels of abstraction?
* How would you simplify the configuration of instrumentations for many deployed apps?
