# Build app
FROM python:3.10-slim
COPY ./app.py .
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

# Run app
ENTRYPOINT [ "python3", "app.py" ]
EXPOSE 4321
