FROM python:3.6

RUN apt-get update && \
    apt-get install --yes python3-dev \
        python3-pip \
        pkg-config

COPY . /mi-salud
WORKDIR /mi-salud

RUN pip install -r requirements.txt
EXPOSE 8000

ENTRYPOINT [ "init-misalud.sh" ]