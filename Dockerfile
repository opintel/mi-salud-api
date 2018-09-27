FROM python:3.6

RUN apt-get update && \
    apt-get install --yes python3-dev \
        python3-pip \
        pkg-config

COPY . /mi-salud
# COPY id_rsa .ssh/id_rsa.pub

WORKDIR /mi-salud

RUN pip install -r requirements.txt && chmod 777 init-misalud.sh
EXPOSE 8000

ENTRYPOINT [ "./init-misalud.sh" ]