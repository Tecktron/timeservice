FROM tecktron/python-bjoern:latest-slim
ARG DEBIAN_FRONTEND=noninteractive

ENV APP_MODULE=timeserver:app

COPY . /app
RUN chmod +x /app/prestart.sh
WORKDIR /app/

RUN python -m pip install pip --no-cache-dir --upgrade
RUN pip install -r /app/requirements.txt
