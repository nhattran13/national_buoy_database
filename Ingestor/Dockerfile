FROM python:3.10-slim

ENV STATION_ID="tplm2"
ENV MODE="stdmet"

WORKDIR /buoy_project

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "/bin/bash", "-c", "python main.py $STATION_ID"]