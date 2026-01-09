# Secondary Coolant Props

This repo contains some fluid property routines for secondary coolants. It is based on the correlations developed by Åke Melinder, 2010 "Properties of Secondary Working Fluids for Indirect Systems" 2nd ed., International Institute of Refrigeration.

This is intended to be a lightweight library that can be easily imported into any other Python tool, with no bulky dependencies.

## Code Quality

[![Pre-commit](https://github.com/NREL/SecondaryCoolantProps/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/NREL/SecondaryCoolantProps/actions/workflows/pre-commit.yml)
[![Tests](https://github.com/NREL/SecondaryCoolantProps/actions/workflows/tests.yml/badge.svg)](https://github.com/NREL/SecondaryCoolantProps/actions/workflows/tests.yml)

Code is checked for style and tests executed by GitHub Actions.

## Documentation

[![Documentation Status](https://readthedocs.org/projects/secondarycoolantprops/badge/?version=latest)](https://secondarycoolantprops.readthedocs.io/en/latest/?badge=latest)

Docs are built from Sphinx on ReadTheDocs.org and are available at https://secondarycoolantprops.readthedocs.io/en/latest/

## Releases

[![PyPIRelease](https://github.com/NREL/SecondaryCoolantProps/actions/workflows/release.yml/badge.svg)](https://github.com/NREL/SecondaryCoolantProps/actions/workflows/release.yml)

When a release is tagged, a GitHub Action workflow will create a Python wheel and upload it to the PyPI server.

To install into an existing Python environment, execute `pip install SecondaryCoolantProps`

Project page: https://pypi.org/project/SecondaryCoolantProps/

## Development

#### Initialize the virtual environment with uv:

`uv sync`

#### Run pre-commit checks:

`uv run pre-commit run -a`

#### Build and publish:

```shell
uv run build
uv publish
```

#### Build the documentation:

`uv run sphinx-build -b html docs docs/_build/html`
