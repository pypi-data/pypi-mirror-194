# Contributing

To setup the development environment and run all tox tasks, we need to install
all supported Python version using [pyenv](https://github.com/pyenv/pyenv):

```bash
pyenv install 3.7.16
pyenv install 3.8.16
pyenv install 3.9.16
pyenv install 3.10.10
pyenv install 3.11.2
```

Install and upgrade required Python packages:

```bash
python -m pip install --upgrade pip flit tox tox-pyenv pylint pre-commit
```

Clone repository from GitHub and setting up the development environment:

```bash
git clone https://github.com/kianmeng/xsget
cd xsget
flit install --symlink
playwright install
```

Show all available tox tasks:

```bash
$ tox -av
...
default environments:
py37    -> testing against python3.7
py38    -> testing against python3.8
py39    -> testing against python3.9
py310   -> testing against python3.10
py311   -> testing against python3.11

additional environments:
cover   -> generate code coverage report in html
doc     -> generate sphinx documentation in html
gettext -> update pot/po/mo files
```

For code linting, we're using `pre-commit`:

```bash
pre-commit install
pre-commit clean
pre-commit run --all-files
```
