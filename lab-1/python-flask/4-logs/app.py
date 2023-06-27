####  OpenTelemetry logs configuration  ########################################
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
logger_provider = LoggerProvider()
logger_provider.add_log_record_processor(BatchLogRecordProcessor(ConsoleLogExporter())) # Remove this in production
#logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter())) # Use this in production
set_logger_provider(logger_provider)

# Logging instrumentation
import logging
handler = LoggingHandler(logger_provider=logger_provider)
logging.getLogger().addHandler(handler)

# Configure app
import flask
app = flask.Flask(__name__)

# Handle requests to http://localhost:4321/error
@app.route('/error')
def error():
    return eval('0/0')

# Handle requests to http://localhost:4321/
@app.route('/')
def home():
    logging.warning('custom-log-message')
    return 'ok'

# Run the app when executing this file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
