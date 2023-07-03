####  OpenTelemetry metrics configuration  #####################################
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
meter_provider = MeterProvider(metric_readers=[
    PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=5000)
])
set_meter_provider(meter_provider)

# Create two custom metrics: counter and histogram
meter = get_meter_provider().get_meter('custom_meter')
counter = meter.create_counter('custom_counter')
histogram = meter.create_histogram('custom_histogram')

# Create a function to generate a random number from 0 to 10,000
from random import randint
def random_number():
    return randint(0, 10000)

# Configure app
import flask
app = flask.Flask(__name__)

# Flask auto-instrumentation
from opentelemetry.instrumentation.flask import FlaskInstrumentor
FlaskInstrumentor().instrument_app(app)

# Handle requests to http://localhost:4321/
@app.route('/')
def home():
    counter.add(1, attributes={ 'foo': 'bar' })
    histogram.record(random_number(), attributes={ 'foo': 'baz' })
    return 'ok'

# Handle requests to http://localhost:4321/error
@app.route('/error')
def error():
    return eval('0/0')

# Run the app when executing this file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
