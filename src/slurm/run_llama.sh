#!/bin/bash

export PIP_INDEX_URL=http://pypi-cache/index
export PIP_TRUSTED_HOST=pypi-cache
export PIP_NO_CACHE=true

export LLAMA_CHECKPOINT_DIR=/ds/models/llms/llama/7B/
export LLAMA_TOKENIZER_PATH=/ds/models/llms/llama/tokenizer.model

cd "$(dirname "$0")"
cd ..

pip install -r ../requirements.txt
pip install -r llm/wrapper/llama/requirements.txt

python3 -m llm.run --llm llama-7b --mode http_api