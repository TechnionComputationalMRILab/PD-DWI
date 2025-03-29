FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update --yes && \
    apt-get install -y python3-pip

ENV POETRY_VERSION=2.1.1
RUN pip3 install --upgrade pip && pip3 install "poetry==$POETRY_VERSION"


RUN mkdir /src
WORKDIR /src

RUN poetry config virtualenvs.create false

# Install dependencies (cached)
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root

COPY . .
RUN poetry install --no-dev --no-interaction --no-ansi

# # Run pd-dwi cli # #
ENTRYPOINT ["pd-dwi"]
