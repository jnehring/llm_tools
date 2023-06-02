# download model and tokenizer to the cache directory

from transformers import GPTNeoXForCausalLM, AutoTokenizer

cache_dir = "/ds/models/llms/cache"
for model_name in ("EleutherAI/pythia-70m-deduped", "EleutherAI/pythia-6.9b"):
  GPTNeoXForCausalLM.from_pretrained(
    model_name,
    cache_dir=cache_dir,
  )

  tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    cache_dir=cache_dir,
  )
