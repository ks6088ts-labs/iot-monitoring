[![test](https://github.com/ks6088ts-labs/iot-monitoring/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/iot-monitoring/actions/workflows/test.yaml?query=branch%3Amain)
[![docker](https://github.com/ks6088ts-labs/iot-monitoring/actions/workflows/docker.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/iot-monitoring/actions/workflows/docker.yaml?query=branch%3Amain)
[![docker-release](https://github.com/ks6088ts-labs/iot-monitoring/actions/workflows/docker-release.yaml/badge.svg)](https://github.com/ks6088ts-labs/iot-monitoring/actions/workflows/docker-release.yaml)

# iot-monitoring

This is a template repository for Python

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [GNU Make](https://www.gnu.org/software/make/)

## Development instructions

### Architecture

[![architecture](docs/architecture.png)](docs/architecture.png)

### How to use

Run the following command to start the project and access Grafana at [http://localhost:3000](http://localhost:3000).

```shell
docker compose up
```

### Local development

Use Makefile to run the project locally.

```shell
# help
make

# install dependencies for development
make install-deps-dev

# run tests
make test

# run CI tests
make ci-test
```

### Docker development

```shell
# build docker image
make docker-build

# run docker container
make docker-run

# run CI tests in docker container
make ci-test-docker
```

To publish the docker image to Docker Hub, you need to set the following secrets in the repository settings.

```shell
gh secret set DOCKERHUB_USERNAME --body $DOCKERHUB_USERNAME
gh secret set DOCKERHUB_TOKEN --body $DOCKERHUB_TOKEN
```
