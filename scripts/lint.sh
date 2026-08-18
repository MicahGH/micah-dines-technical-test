#!/usr/bin/env bash
black .

ruff check . --fix

pyright .