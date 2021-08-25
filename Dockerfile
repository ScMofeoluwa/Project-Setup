FROM python:latest
WORKDIR /app
ADD . .
RUN pip install fastapi
