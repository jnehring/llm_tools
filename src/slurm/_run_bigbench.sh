#!/bin/bash

cd /netscratch/nehring/projects/industry/llm_tools/src/slurm
nohup ./run_llm.sh $1 &

sleep 120

export PIP_INDEX_URL=http://pypi-cache/index
export PIP_TRUSTED_HOST=pypi-cache
export PIP_NO_CACHE=true

pip install -r /netscratch/nehring/projects/industry/BIG-bench/requirements.txt

cd /netscratch/nehring/projects/industry/BIG-bench && python -m run_all_tasks.py $1