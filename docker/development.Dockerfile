FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update --yes && \
    apt-get install -y python3-pip git

ENV POETRY_VERSION=1.8.3
RUN pip3 install --upgrade pip && pip3 install "poetry==$POETRY_VERSION"


RUN mkdir /src
WORKDIR /src

RUN poetry config virtualenvs.create true

# Install dependencies (cached)
COPY pyproject.toml poetry.lock README.md ./
RUN poetry install

CMD ["/bin/bash"]
