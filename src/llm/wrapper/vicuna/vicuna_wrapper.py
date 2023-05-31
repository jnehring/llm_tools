from llm.wrapper.llm_wrapper import LLMWrapper
from transformers import LlamaForCausalLM, LlamaTokenizer
import os

class VicunaWrapper(LLMWrapper):

    def __init__(self, app):
        self.model = LlamaForCausalLM.from_pretrained(os.getenv("MODEL_PATH"))
        self.tokenizer = LlamaTokenizer.from_pretrained(os.getenv("LLAMA_TOKENIZER_PATH"))

    def generate_response(self, input_str : str):
        inputs = self.tokenizer(input_str, return_tensors="pt")
        tokens = self.model.generate(**inputs)
        return self.tokenizer.decode(tokens[0])




