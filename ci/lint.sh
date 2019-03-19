#!/usr/bin/env bash
set -xe

pycodestyle                    app migrations/versions tests
isort --check-only --recursive app migrations/versions tests
pyflakes                       app migrations/versions tests
flake8                         app migrations/versions tests
mypy                           app migrations/versions tests
