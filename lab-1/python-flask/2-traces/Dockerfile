# Build app
FROM python:3.10-slim
COPY ./app.py .
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

# OpenTelemetry configuration
ARG OTEL_SERVICE_NAME
ENV OTEL_SERVICE_NAME=${OTEL_SERVICE_NAME:-python-flask}

# Run app
ENTRYPOINT [ "python3", "app.py" ]
EXPOSE 4321
