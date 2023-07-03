####  OpenTelemetry traces configuration  ######################################
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import set_tracer_provider
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
set_tracer_provider(tracer_provider)

####  OpenTelemetry metrics configuration  #####################################
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
meter_provider = MeterProvider(metric_readers=[
    PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=5000)
])
set_meter_provider(meter_provider)

####  OpenTelemetry logs configuration  ########################################
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
logger_provider = LoggerProvider()
logger_provider.add_log_record_processor(BatchLogRecordProcessor(ConsoleLogExporter()))
set_logger_provider(logger_provider)

# Logging instrumentation
import logging
handler = LoggingHandler(logger_provider=logger_provider)
logger = logging.getLogger()
logger.addHandler(handler)

# Configure app
import flask
app = flask.Flask(__name__)

# Flask auto-instrumentation
from opentelemetry.instrumentation.flask import FlaskInstrumentor
FlaskInstrumentor().instrument_app(app)

# Handle requests to http://localhost:4321/
@app.route('/')
def home():
    return 'ok'

# Handle requests to http://localhost:4321/error
@app.route('/error')
def error():
    return eval('0/0')

# Run the app when executing this file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
