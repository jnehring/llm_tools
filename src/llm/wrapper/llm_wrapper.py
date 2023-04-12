from abc import ABC, abstractmethod
import numpy as np
import os
import openai
import requests

class LLMWrapper(ABC):

    @abstractmethod
    def generate_response(self, input_str : str, max_tokens : int=10 , temperature : float = 0):
        pass

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

class OpenAIDavinci(LLMWrapper):

    def generate_response(self, input_str : str, max_tokens : int =10 , temperature : float = 0):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=input_str,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response["choices"][0]["text"]

class RemoteHTTPLLM(LLMWrapper):

    def __init__(self, api_url):
        self.api_url = api_url

    def generate_response(self, input_str : str, max_tokens : int =10 , temperature : float = 0):
        doc = {"doc": input_str}
        x = requests.post(self.api_url, json = doc)
        return x.text
