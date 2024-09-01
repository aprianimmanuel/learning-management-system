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
        gnupg \
        curl \
        libxml2-dev \
        libxmlsec1-dev \
        libxmlsec1-openssl \
        libpq-dev \
        g++ \
        gcc \
        git \
        python3-dev \
        python3-wheel \
        python3-pip \
        python3-venv \
        python3-distutils \
        build-essential \
        wget \
        unzip && \
    # Set up Python environment
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

# Set permissions for application files
RUN mkdir -p /backend/logs /backend/apps && \
    touch /backend/logs/debug.log && \
    chmod 666 /backend/logs/debug.log && \
    chown -R $DJANGO_USER:$DJANGO_USER $VENV_PATH /backend /backend/apps /backend/logs

COPY ./apps /backend/apps

ENV PATH="$VENV_PATH/bin:$PATH"

USER $DJANGO_USER
