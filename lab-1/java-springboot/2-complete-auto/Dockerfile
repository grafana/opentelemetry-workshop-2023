# Build app
FROM maven:3.8.5-openjdk-11 AS maven_build
COPY pom.xml /tmp/
COPY src /tmp/src/
WORKDIR /tmp/
RUN mvn package
FROM eclipse-temurin:11
COPY --from=maven_build /tmp/target/app-0.1.0.jar /data/app-0.1.0.jar

# OpenTelemetry configuration
ARG OTEL_EXPORTER_OTLP_ENDPOINT
ARG OTEL_SERVICE_NAME
ENV OTEL_EXPORTER_OTLP_ENDPOINT=${OTEL_EXPORTER_OTLP_ENDPOINT:-http://localhost:4318}
ENV OTEL_SERVICE_NAME=${OTEL_SERVICE_NAME:-java-springboot}

# Change "logging" to "otlp" in production
ARG OTEL_TRACES_EXPORTER
ARG OTEL_METRICS_EXPORTER
ARG OTEL_LOGS_EXPORTER
ARG OTEL_SERVICE_NAME
ENV OTEL_TRACES_EXPORTER=${OTEL_TRACES_EXPORTER:-logging}
ENV OTEL_METRICS_EXPORTER=${OTEL_METRICS_EXPORTER:-logging}
ENV OTEL_LOGS_EXPORTER=${OTEL_LOGS_EXPORTER:-logging}
ENV OTEL_SERVICE_NAME=${OTEL_SERVICE_NAME:-java-springboot}

# Instrument app
ADD https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v1.27.0/opentelemetry-javaagent.jar .
ENV JAVA_TOOL_OPTIONS "-javaagent:./opentelemetry-javaagent.jar"

# Run app
ENV JAVA_OPTS "-Dlogging.level.org.springframework.web.filter.CommonsRequestLoggingFilter=DEBUG"
CMD java -jar /data/app-0.1.0.jar --server.port=4321 --debug
EXPOSE 4321
