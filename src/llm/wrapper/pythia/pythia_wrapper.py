from transformers import GPTNeoXForCausalLM, AutoTokenizer
from llm.wrapper.llm_wrapper import LLMWrapper

class PythiaWrapper(LLMWrapper):

    def __init__(self):
        model_name = "EleutherAI/pythia-6.9b"
        cache_dir = "/ds/models/llms/cache"
        self.model = GPTNeoXForCausalLM.from_pretrained(
            model_name,
            cache_dir=cache_dir,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=cache_dir
        )


    def generate_response(self, input_str : str):
        inputs = self.tokenizer(input_str, return_tensors="pt")
        tokens = self.model.generate(**inputs)
        return tokenizer.decode(tokens[0])




