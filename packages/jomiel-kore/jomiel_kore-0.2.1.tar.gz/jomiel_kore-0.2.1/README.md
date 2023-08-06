# jomiel-kore

[![pypi-pyversions](https://img.shields.io/pypi/pyversions/jomiel-kore?color=%230a66dc)][pypi]
[![pypi-v](https://img.shields.io/pypi/v/jomiel-kore?color=%230a66dc)][pypi]
[![pypi-wheel](https://img.shields.io/pypi/wheel/jomiel-kore?color=%230a66dc)][pypi]
[![pypi-status](https://img.shields.io/pypi/status/jomiel-kore?color=%230a66dc)][pypi]
[![code-style](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi]: https://pypi.org/project/jomiel-kore
[black]: https://pypi.org/project/black

The minimalistic foundation for creating new [Python] applications.

## Requirements

`jomiel-kore` is written for [Python] 3.6 and later.

[python]: https://www.python.org/about/gettingstarted/

## Installation

```shell
pip install jomiel-kore
```

Install from the repository, e.g. for development:

```shell
git clone https://github.com/guendto/jomiel-kore
cd jomiel-kore
pip install -e .  # Install a project in editable mode
```

Or, if you'd rather not install in "editable mode":

```shell
pip install git+https://github.com/guendto/jomiel-kore
```

## License

`jomiel-kore` is licensed under the [Apache License version 2.0][aplv2].

[aplv2]: https://www.tldrlegal.com/l/apache2

## Acknowledgements

- [pre-commit] is used for linting and reformatting, see the
  [.pre-commit-config.yaml] file

[.pre-commit-config.yaml]: https://github.com/guendto/jomiel-kore/blob/master/.pre-commit-config.yaml
[pre-commit]: https://pre-commit.com/
