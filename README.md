# Gen AI Case Study

## Overview

Vectorize the Frankendstein PDF book into the chromadb database. Use LLM to ask the defined question against the book. Use LLM to evaluate if the answer is sufficient.

Complete the tasks in the files and run the code, the evaluation should pass. Create a git commit for all code/config changes and zip entire folder contents, excluding venv/data folders. Also attach terminal text output of the execution.

## Environment Setup

Requirements:

- docker
- poetry
- vscode

## 1. Ingest (`./src/app/ingest.py`)

Instructions are in the file under the `TASK` comment.

## 2. Query (`./src/app/query.py`)

Instructions are in the file under the `TASK` comment.

## 3. Evaluate (`./src/app/evaluate.py`)

Instructions are in the file under the `TASK` comment.

## Local LLM Setup

The local LLM will run in docker of Ollama via the `./docker-compose.yml`.

```shell
docker compose up
```

In another terminal execute to install and run `llama2`.

```shell
docker exec -it ollama ollama run llama2
```

## Poetry Env

```shell
# Start poetry environment shell in terminal
poetry shell

# Install project dependencies
poetry install

# Run __main__.py
app run
```