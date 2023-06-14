from llm.wrapper.llm_wrapper import HuggingFaceLLMWrapper
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

class AutoModelWrapper(HuggingFaceLLMWrapper):

    def __init__(self, app):
        HuggingFaceLLMWrapper.__init__(self)

        assert app.get_args().huggingface_model is not None

        model_name= app.get_args().huggingface_model

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=os.getenv("HUGGINGFACE_CACHE_DIR")
        ).cuda()

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=os.getenv("HUGGINGFACE_CACHE_DIR")
        )
