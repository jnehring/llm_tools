from llm.wrapper.huggingface_wrapper import HuggingFaceLLMWrapper
from transformers import LlamaForCausalLM, LlamaTokenizer
import os

class VicunaWrapper(HuggingFaceLLMWrapper):

    def __init__(self, app):
        HuggingFaceLLMWrapper.__init__(self)
        self.model = LlamaForCausalLM.from_pretrained(
            os.getenv("MODEL_PATH"),
            device_map="auto"
        )
        self.tokenizer = LlamaTokenizer.from_pretrained(os.getenv("LLAMA_TOKENIZER_PATH"))
        self.tokenizer.pad_token = self.tokenizer.eos_token
