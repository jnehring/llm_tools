from llm.wrapper.llm_wrapper import HuggingFaceLLMWrapper
from transformers import LlamaForCausalLM, LlamaTokenizer
import os

class VicunaWrapper(HuggingFaceLLMWrapper):

    def __init__(self, app):
        HuggingFaceLLMWrapper.__init__(self)
        self.model = LlamaForCausalLM.from_pretrained(os.getenv("MODEL_PATH")).cuda()
        self.tokenizer = LlamaTokenizer.from_pretrained(os.getenv("LLAMA_TOKENIZER_PATH"))
