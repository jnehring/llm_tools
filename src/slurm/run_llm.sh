#!/bin/bash

export PIP_INDEX_URL=http://pypi-cache/index
export PIP_TRUSTED_HOST=pypi-cache
export PIP_NO_CACHE=true
export HUGGINGFACE_CACHE_DIR=/ds/models/llms/cache

cd "$(dirname "$0")"

pip install -r ../../requirements.txt

model_name=$1

model_type=`bash -c "jq -r '. | .$model_name.wrapper' models.json"`

# set environment variables of model
values=$(jq -r " . | .$model_name.env " models.json)
$( echo "$values" | jq -r 'keys[] as $k | "export \($k)=\(.[$k])"' )

cd ..

echo "Loading model with type $model_type"

if [ "$model_type" = "llama" ]; then
    pip install -r llm/wrapper/llama/requirements.txt
    python3 -m llm.run --wrapper llama

elif [ "$model_type" = "automodel" ]; then
    pip install -r llm/wrapper/automodel/requirements.txt
    model=`bash -c "jq -r '. | .$model_name.model' slurm/models.json"`
    echo "starting automodel with model=$model"
    bash -c "python3 -m llm.run --wrapper automodel --model $model"

elif [ "$model_type" = "t5" ]; then
    pip install -r llm/wrapper/t5/requirements.txt
    model=`bash -c "jq -r '. | .$model_name.model' slurm/models.json"`
    echo "starting t5 with model=$model"
    bash -c "python3 -m llm.run --wrapper t5 --model $model"

elif [ "$model_type" = "vicuna" ]; then
    pip install -r llm/wrapper/vicuna/requirements.txt
    python3 -m llm.run --wrapper vicuna

else
    echo "cannot find configuration for model $model_type"
fi