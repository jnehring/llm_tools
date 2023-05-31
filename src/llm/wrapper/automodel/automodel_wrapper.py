from llm.wrapper.llm_wrapper import LLMWrapper
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

class AutoModelWrapper(LLMWrapper):

    def __init__(self, app):

        assert app.get_args().huggingface_model is not None

        model_name= app.get_args().huggingface_model

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=os.getenv("HUGGINGFACE_CACHE_DIR")
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=os.getenv("HUGGINGFACE_CACHE_DIR")
        )

    def generate_response(self, input_str : str):
        inputs = self.tokenizer(input_str, return_tensors="pt")
        tokens = self.model.generate(**inputs)
        return self.tokenizer.decode(tokens[0])




