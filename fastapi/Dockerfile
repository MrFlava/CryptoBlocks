FROM python:3.10.5

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/src

WORKDIR /src

RUN apt update \
    && apt install -y --no-install-recommends less

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
