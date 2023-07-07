####  OpenTelemetry traces configuration  ######################################
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import set_tracer_provider
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
set_tracer_provider(tracer_provider)

# Configure app
import flask
app = flask.Flask(__name__)

# Flask auto-instrumentation
from opentelemetry.instrumentation.flask import FlaskInstrumentor
FlaskInstrumentor().instrument_app(app)

# Requests auto-instrumentation
import requests
from opentelemetry.instrumentation.requests import RequestsInstrumentor
RequestsInstrumentor().instrument()

# Handle requests to http://localhost:4321/
@app.route('/')
def home():
    requests.get(f'http://localhost:4321/test')
    return 'ok'
    
# Handle requests to http://localhost:4321/test
@app.route('/test')
def test():
    return 'test'

# Handle requests to http://localhost:4321/error
@app.route('/error')
def error():
    return eval('0/0')

# Run the app when executing this file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
