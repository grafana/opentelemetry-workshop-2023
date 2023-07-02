####  OpenTelemetry metrics configuration  #####################################
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
meter_provider = MeterProvider(metric_readers=[
    PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=5000)
])
set_meter_provider(meter_provider)

# Create a custom counter metric
meter = get_meter_provider().get_meter('custom_meter')

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
