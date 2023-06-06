from llm.wrapper.llm_wrapper import HuggingFaceLLMWrapper
from transformers import T5Tokenizer, T5Model
import os

class T5Wrapper(HuggingFaceLLMWrapper):

    def __init__(self, app):
        HuggingFaceLLMWrapper.__init__(self)

        assert app.get_args().huggingface_model is not None

        cache_dir = os.getenv("HUGGINGFACE_CACHE_DIR")

        model_name= app.get_args().huggingface_model

        assert model_name in ("t5-base")
        self.tokenizer = T5Tokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        self.model = T5Model.from_pretrained(model_name, cache_dir=cache_dir)

