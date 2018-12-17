#!/bin/sh

pytest --cov-report=term-missing --cov=morpho tests
mypy --ignore-missing-imports morpho
