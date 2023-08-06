# Apache Airflow Provider for Bacalhau

This is the `bacalhau-airflow`, a python package including an Apache Airflow provider.

What's a provider???

## Features

- Create Airflow tasks that run on Bacalhau (via custom operator!)
- Support for sharded jobs: output shards can be passed downstream (via XComs)
- Coming soon...
    - Lineage (OpenLineage)
    - Various working code examples
    - Hosting instructions

## Requirements

- Python 3.8+
- `bacalhau-sdk` XX
- `apache-airflow` +2.4

## Installation

## From pypi

```console
pip install bacalhau-airflow
```

## From source

Clone the public repository:

```shell
$ git clone https://github.com/bacalhau-project/bacalhau/
```

Once you have a copy of the source, you can install it with:

```shell
$ cd integration/airflow/
$ pip install .
```


## Usage (WIP :warning:)

```
AIRFLOW_VERSION=2.4.1
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

export AIRFLOW_HOME=~/airflow
airflow db init
```

```
export AIRFLOW_HOME=~/airflow
airflow standalone
```


## Development


```shell
$ pip install -r dev-requirements.txt
```

### Unit tests


```shell
$ tox
```

You can also skip using `tox` and run `pytest` on your own dev environment.

