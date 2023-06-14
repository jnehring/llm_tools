# skripts to create the vicuna model from llama downloaded model
# from here https://github.com/lm-sys/FastChat#vicuna-weights

# convert llama model to huggingface format
python -m transformers.models.llama.convert_llama_weights_to_hf \
    --input_dir /ds/models/llms/llama/ --model_size 13B --output_dir /ds/models/llms/llama_hf/13B/

# create vicuna out of llama
python3 -m fastchat.model.apply_delta \
    --base-model-path /ds/models/llms/llama_hf/13B/ \
    --target-model-path /ds/models/llms/vicuna/13B \
    --delta-path lmsys/vicuna-13b-delta-v1.1
