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


## Ollama Response
>>> Succinctly summarize what disturbes Victor's sleep?

Victor is disturbed by the cawing of crows outside his window, which keeps him awake and prevents him from falling asleep.
![images][ollama_response.png]


## llama2 trained model Response(local RAG)
sentence_collection 79c048a2-00da-48f3-9280-40dfb2f26bd3
nodes_collection d5ff5657-7110-4b74-bbe2-8dd18e6c956c
response Victor's sleep is disturbed by the thoughts of his brother William's death, which he learned through a letter from their father.
response Victor's inability to sleep is due to his watching and misery.
[2024-04-24 19:32:04,950] INFO [main:25] Query response: Victor's inability to sleep is due to his watching and misery.
sentence_collection 79c048a2-00da-48f3-9280-40dfb2f26bd3
nodes_collection d5ff5657-7110-4b74-bbe2-8dd18e6c956c
True
query="Succinctly summarize what disturbes Victor's sleep?" contexts=['I had been awake the \nwhole of the preceding night, my nerves were agitated, and \nmy eyes inflamed by watching and misery. ', '‘Pardon this intrusion,’ said I; ‘I am a traveller \nin want of a little rest; you would greatly oblige me if you \nwould allow me to remain a few minutes before the fire.’\n‘‘Enter,’ said De Lacey, ‘and I will try in what manner I \ncan to relieve your wants; but, unfortunately, my children \nare from home, and as I am blind, I am afraid I shall find it \ndifficult to procure food for you.’\n‘‘Do not trouble yourself, my kind host; I have food; it is \nwarmth and rest only that I need.’'] response="Victor's inability to sleep is due to his watching and misery." passing=True feedback='YES' score=1.0 pairwise_source=None invalid_result=False invalid_reason=None
[2024-04-24 19:35:45,788] INFO [main:33] Evaluated: True
[2024-04-24 19:35:45,789] INFO [main:35] Complete.

![images][llama2_response.png]


