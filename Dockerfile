FROM python:3.10-slim

ENV STATION_ID="tplm2"
ENV YEAR="2024"

WORKDIR /buoy_project

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/bin/bash", "-c", "python Ingestor/main.py \"$STATION_ID\" \"$YEAR\""]
