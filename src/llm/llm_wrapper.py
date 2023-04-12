from abc import ABC, abstractmethod

class LLMWrapper(ABC):

    @abstractmethod
    def generate_response(self, input_str : str, max_tokens : int=10 , temperature : float = 0):
        pass

