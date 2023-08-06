FROM python:3.9.13

ENV PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt /tmp/requirements/

RUN pip install -r /tmp/requirements/requirements.txt

COPY . .

CMD ["bash"]