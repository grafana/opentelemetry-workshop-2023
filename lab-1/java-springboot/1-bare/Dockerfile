# Build app
FROM maven:3.8.5-openjdk-11 AS maven_build
COPY pom.xml /tmp/
COPY src /tmp/src/
WORKDIR /tmp/
RUN mvn package
FROM eclipse-temurin:11
COPY --from=maven_build /tmp/target/app-0.1.0.jar /data/app-0.1.0.jar

# Run app
ENV JAVA_OPTS "-Dlogging.level.org.springframework.web.filter.CommonsRequestLoggingFilter=DEBUG"
CMD java -jar /data/app-0.1.0.jar --server.port=4321 --debug
EXPOSE 4321
