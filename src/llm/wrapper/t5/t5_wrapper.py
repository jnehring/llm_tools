from llm.wrapper.llm_wrapper import HuggingFaceLLMWrapper
from transformers import T5Tokenizer, T5Model, T5ForConditionalGeneration
import os

class T5Wrapper(HuggingFaceLLMWrapper):

    def __init__(self, app):
        HuggingFaceLLMWrapper.__init__(self)

        assert app.get_args().huggingface_model is not None

        cache_dir = os.getenv("HUGGINGFACE_CACHE_DIR")

        model_name= app.get_args().huggingface_model

        # assert model_name in ("t5-base")
        self.tokenizer = T5Tokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        if model_name in ("t5-base"):
            self.model = T5Model.from_pretrained(model_name, cache_dir=cache_dir, device_map="auto")
        elif model_name in ("google/flan-t5-large"):
            self.model = T5ForConditionalGeneration.from_pretrained(model_name, cache_dir=cache_dir, device_map="auto").cuda()


        

