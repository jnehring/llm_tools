from llm.wrapper.huggingface_wrapper import HuggingFaceLLMWrapper
from transformers import T5Tokenizer, T5Model, T5ForConditionalGeneration
import os

class T5Wrapper(HuggingFaceLLMWrapper):

    def __init__(self, app):
        HuggingFaceLLMWrapper.__init__(self)

        assert app.get_args().model is not None

        cache_dir = os.getenv("HUGGINGFACE_CACHE_DIR")

        model_name= app.get_args().model

        self.tokenizer = T5Tokenizer.from_pretrained(model_name, cache_dir=cache_dir)

        google_prefix = "google/flan-t5"

        if model_name in ("t5-base"):
            self.model = T5Model.from_pretrained(model_name, cache_dir=cache_dir, device_map="auto")
        elif model_name in ("google/flan-t5-base", "google/flan-t5-large", "google/flan-t5-xl", "google/flan-t5-xxl"):
            self.model = T5ForConditionalGeneration.from_pretrained(model_name, cache_dir=cache_dir, device_map="auto")
        else:
            raise Exception(f"model \"{model_name}\" not supported")

        

