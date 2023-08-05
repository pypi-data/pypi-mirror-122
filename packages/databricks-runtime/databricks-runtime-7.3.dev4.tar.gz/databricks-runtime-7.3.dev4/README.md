# Databricks LTS Python Runtimes

This repository contains a simple python package `runtime` to facilitate
referencing the supported python libraries in the [long-term support
databricks runtimes](https://docs.databricks.com/release-notes/runtime/releases.html).

This should facilitate adding the LTS dependencies in external python projects,
specially when building python wheels.

## Installation

Install via pip:

```
pip install databricks-runtime==7.3.dev4
```

## Development

Clone this repo and install locally with:

```commandline
$ pip install -e .
```

Install the development reqs:

```commandline
$ pip install -r requirements-development.txt
```

Tools & common scripts:
* Style check: `bash check-style.sh`
* Type check: `bash check-types.sh`
* Profiles: `bash profiler.sh`

## Supported LTS Versions

### 7.3 LTS

Reference to official documentation [here](https://docs.databricks.com/release-notes/runtime/7.3.html).
* Python version: `3.7.5`
* Release date: `Sep 24, 2020`

