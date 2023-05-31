from llm.wrapper.llm_wrapper import LLMWrapper
from transformers import LlamaForCausalLM, LlamaTokenizer
import os

class VicunaWrapper(LLMWrapper):

    def __init__(self, app):

        assert app.get_args().huggingface_model is not None

        model_name= app.get_args().huggingface_model

        self.model = LlamaForCausalLM.from_pretrained(model_name)

        self.tokenizer = LlamaTokenizer.from_pretrained()

    def generate_response(self, input_str : str):
        inputs = self.tokenizer(input_str, return_tensors="pt")
        tokens = self.model.generate(**inputs)
        return self.tokenizer.decode(tokens[0])




