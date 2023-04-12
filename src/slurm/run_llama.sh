#!/bin/bash

export PIP_INDEX_URL=http://pypi-cache/index
export PIP_TRUSTED_HOST=pypi-cache
export PIP_NO_CACHE=true

cd "$(dirname "$0")"
cd ..

pip install -r ../requirements.txt
pip install -r llm/wrapper/llama/requirements.txt

python3 -m llm.run --llm llama-7b --mode http_api