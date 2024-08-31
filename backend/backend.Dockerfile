FROM python:3.12-bookworm
LABEL maintainer="immanuelaprian@gmail.com"

ENV PYTHONUNBUFFERED=1 \
    VENV_PATH=/py

WORKDIR /backend
EXPOSE 7555

COPY ./requirement/requirements.txt /tmp/requirements.txt
COPY ./requirement/requirements.dev.txt /tmp/requirements.dev.txt

ARG DEV=false
ARG DJANGO_USER
ARG DJANGO_UID
ARG DJANGO_GID

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
        tzdata \
        ntpdate \
        postgresql-common \
        pkg-config \
        python3-dev \
        python3-wheel \
        python3-pip \
        wget \
        unzip && \
    python3 -m venv $VENV_PATH && \
    $VENV_PATH/bin/pip install --upgrade pip && \
    $VENV_PATH/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        $VENV_PATH/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* /usr/share/man/* /usr/share/locale/* /usr/share/info/* && \
    find /usr/lib -type f -name '*.a' -delete && \
    find /usr/include -type f -name '*.h' -delete && \
    groupadd -g $DJANGO_GID $DJANGO_USER && \
    useradd -m -u $DJANGO_UID -g $DJANGO_GID $DJANGO_USER

