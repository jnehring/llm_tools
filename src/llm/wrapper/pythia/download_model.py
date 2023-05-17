# download model and tokenizer to the cache directory

from transformers import GPTNeoXForCausalLM, AutoTokenizer

model_name = "EleutherAI/pythia-6.9b"
cache_dir = "/ds/models/llms/cache"
GPTNeoXForCausalLM.from_pretrained(
  model_name,
  cache_dir=cache_dir,
)

tokenizer = AutoTokenizer.from_pretrained(
  model_name,
  cache_dir=cache_dir,
)
