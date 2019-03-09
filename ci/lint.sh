#!/usr/bin/env bash
set -xe

pycodestyle                    app tests
isort --check-only --recursive app tests
pyflakes                       app tests
flake8                         app tests
mypy                           app tests
