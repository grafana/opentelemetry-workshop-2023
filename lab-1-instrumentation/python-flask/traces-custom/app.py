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

# Use custom tracer
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
tracer = trace.get_tracer(__name__)

# Create a greeting message
@tracer.start_as_current_span('child_span_2')
def greeting():
    greeting = 'hello!'
    trace.get_current_span().set_attribute('greeting', greeting)
    return greeting

# Handle requests to http://localhost:4321/
@app.route('/')
def home():
    parent_span = trace.get_current_span()
    with tracer.start_as_current_span('child_span_1') as child_span:
        message = greeting()
    parent_span.add_event('we made a friend', { 'mood': 'happy' })
    parent_span.set_status(Status(StatusCode.OK))
    return message

# Handle requests to http://localhost:4321/error
@app.route('/error')
def error():
    return eval('0/0')

# Run the app when executing this file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
