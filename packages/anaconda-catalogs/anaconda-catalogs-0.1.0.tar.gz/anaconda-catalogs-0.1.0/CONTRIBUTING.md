# Contributing guide

## Local development setup

### Create a virtual environment & install dev dependencies

```shell
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Set up `pre-commit`

```shell
pre-commit install
```

### To build the conda package

To build the conda package, ensure `conda-build` is installed into your base environment:

```shell
conda install conda-build
```

Then, from the repository base directory, run:

```shell
conda build conda.recipe
```
