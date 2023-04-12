import numpy as np

from llm.wrapper.llm_wrapper import LLMWrapper

class DummyLLM(LLMWrapper):

    def __init__(self):
        self.responses = [
            "Hello, I am the Dummy LLM.",
            "I say random stuff.",
            "I am the smartest LLM of all."
        ]
        
    def generate_response(self, input_str : str, max_tokens : int =10 , temperature : float = 0):
        response = np.random.choice(self.responses)
        response += "\n\nYour input was: " + input_str
        return response

