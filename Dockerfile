FROM python:3.10-slim

WORKDIR /buoy_project

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY python_files/ ./python_files/


