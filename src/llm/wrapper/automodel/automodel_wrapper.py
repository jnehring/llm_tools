from llm.wrapper.huggingface_wrapper import HuggingFaceLLMWrapper
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

class AutoModelWrapper(HuggingFaceLLMWrapper):

    def __init__(self, app):
        HuggingFaceLLMWrapper.__init__(self)

        assert app.get_args().model is not None

        model_name= app.get_args().model

        trust_remote_code = os.getenv("TRUST_REMOTE_CODE", default=False)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=os.getenv("HUGGINGFACE_CACHE_DIR"),
            trust_remote_code=trust_remote_code,
            device_map="auto"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=os.getenv("HUGGINGFACE_CACHE_DIR")
        )
