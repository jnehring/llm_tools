#!/bin/bash

export PIP_INDEX_URL=http://pypi-cache/index
export PIP_TRUSTED_HOST=pypi-cache
export PIP_NO_CACHE=true
export HUGGINGFACE_CACHE_DIR=/ds/models/llms/cache

cd "$(dirname "$0")"

pip install -r ../../requirements.txt

pwd

model_name=$1

model_type=`bash -c "jq '. | .$model_name.llm' models.json"`

# set environment variables of model
values=$(jq -r " . | .$model_name.env " models.json)
$( echo "$values" | jq -r 'keys[] as $k | "export \($k)=\(.[$k])"' )

cd ..
if [ $model_type=="llama" ]; then
    pip install -r llm/wrapper/llama/requirements.txt
    python3 -m llm.run --llm llama --mode http_api
elif [$model_type=="automodel"]; then
    pip install -r llm/wrapper/automodel/requirements.txt
    huggingface_model = bash -c "jq '. | .$model_name.huggingface-model' models.json"
    bash -c "python3 -m llm.run --llm $huggingface_model --mode http_api"
fi