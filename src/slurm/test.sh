#!/bin/bash

model_name="vicuna13b"

#values = ""
#"$(jq -r " . | .$model_name.env " models.json)" | $values
#echo $values


values=$(jq -r " . | .$model_name.env " models.json)
echo $values
#values='{"MODEL_PATH": "/ds/models/llms/vicuna/13B", "LLAMA_TOKENIZER_PATH": #"/ds/models/llms/llama/tokenizer.model" }'
$( echo "$values" | jq -r 'keys[] as $k | "export \($k)=\(.[$k])"' )

#for s in $(echo $values | jq -r "to_entries|map(\"\(.key)=\(.value|tostring)\")|.[]" ); do
#    echo $s
#    bash -c "export $s"
#    export $s
#done

echo $MODEL_PATH

#bash -c "jq -r '. | .$model_name.env | keys[] ' models.json" | while read key ; do
#    #"$key"  | tr -d '"' | $key
#    echo $key
#    # value = "$(jq -r " . | .$model_name.env.$key " models.json)"
#    value = "$(jq -r ' .vicuna13b.env.MODEL_PATH ' models.json)"
#    #echo $key
#    echo $value
#    #bash -c "export $key=$value"
#    #bash -c "export $key=$value"
#done