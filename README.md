[![Build](https://github.com/nacifyas/atomflare_web/actions/workflows/flake8-mypy-build.yaml/badge.svg)](https://github.com/nacifyas/atomflare_web/actions/workflows/flake8-mypy-build.yaml)
[![CodeQL](https://github.com/nacifyas/atomflare_web/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/nacifyas/atomflare_web/actions/workflows/codeql-analysis.yml)
# Atomflare Web

This poject contains the backend for a webapp, that stores services & users. The intention behind this project is to keep track of my internet projects under the domain Atomflare.tk

In order to test this project, a test db by postgres is requiered.
You do not neet to create the specific tables, just change the url at database.py according to your needs, and uncomment the code at main.py, and you will be ready to go.

Run the file main.py and go to 127.0.0.1:8000/docs and you will be prompted with the API documentation.
