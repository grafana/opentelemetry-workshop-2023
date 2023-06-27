####  OpenTelemetry metrics configuration  #####################################
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
meter_provider = MeterProvider(metric_readers=[
    PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=5000), # Remove this in production
    #PeriodicExportingMetricReader(OTLPMetricExporter(), export_interval_millis=5000) # Use this in production
])
set_meter_provider(meter_provider)

# Create a custom counter metric
meter = get_meter_provider().get_meter('custom_meter')
counter = meter.create_counter('custom_counter')

# Configure app
import flask
app = flask.Flask(__name__)

# Handle requests to http://localhost:4321/
@app.route('/')
def home():
    counter.add(1) # Invoke custom metric counter
    return 'ok'

# Handle requests to http://localhost:4321/error
@app.route('/error')
def error():
    return eval('0/0')

# Run the app when executing this file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
