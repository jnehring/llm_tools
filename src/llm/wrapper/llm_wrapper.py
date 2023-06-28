from abc import ABC, abstractmethod
import numpy as np
import os
import openai
import requests
import json
from typing import Dict
import logging

class LLMWrapper(ABC):

    def __init__(self):
        self.params = {
            "max_new_tokens": lambda x : int(x),
            "temperature": lambda x: float(x),
            "skip_special_tokens": lambda x : bool(x)
        }

    @abstractmethod
    def generate_response(self, input_str : str, args : Dict):
        pass

    def clean_args(self, args):
        # remove args that are not defined in self.params
        valid_keys = filter(lambda x : x in self.params.keys(), args.keys())
        args = {key: args[key] for key in valid_keys}
        # get args
        args = {key: self.params[key](value) for key, value in args.items()}
        return args

class HuggingFaceLLMWrapper(LLMWrapper):

    def __init__(self):
        LLMWrapper.__init__(self)

    def generate_response(self, input_str : str, args : Dict):
        clean_args = self.clean_args(args)
        inputs = self.tokenizer(input_str, return_tensors="pt")

        # remove all arguments that the model does not accept
        for key in list(inputs.keys()):
            if key not in self.model.generate.__code__.co_varnames:
                del inputs[key]

        for key in inputs.keys():
            inputs[key] = inputs[key].cuda()
        for key, value in clean_args.items():
            inputs[key] = value
        tokens = self.model.generate(**inputs)

        key = "skip_special_tokens"
        skip_special_tokens = args[key] if key in args.keys() else True
        return self.tokenizer.decode(tokens[0], skip_special_tokens=skip_special_tokens)

class DummyLLM(LLMWrapper):

    def __init__(self):
        LLMWrapper.__init__(self)
        self.responses = [
            "Hello, I am the Dummy LLM.",
            "I say random stuff.",
            "I am the smartest LLM of all."
        ]

    def generate_response(self, input_str : str, args):
        args = self.clean_args(args)
        response = np.random.choice(self.responses)
        response += "\n\nYour input was: " + input_str + "\n, the arguments were " + str(args)
        return response

class OpenAIDavinci(LLMWrapper):

    def __init__(self):
        LLMWrapper.__init__(self)

    def generate_response(self, input_str : str, args):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        openai_args = {
            "model": "text-davinci-003",
            "prompt": input_str,
        }

        if "max_new_tokens" in args.keys():
            openai_args["max_tokens"] = args["max_new_tokens"]

        if "temperature" in args.keys():
            openai_args["temperature"] = args["temperature"]


        response = openai.Completion.create(**openai_args)
        return response["choices"][0]["text"]

class RemoteHTTPLLM(LLMWrapper):

    def __init__(self, api_url):
        self.api_url = api_url

    def generate_response(self, input_str : str, args):
        doc = {"doc": input_str}
        x = requests.post(self.api_url, json = doc)
        return x.text
    
class OPENGPTX(LLMWrapper):

    def __init__(self):
        LLMWrapper.__init__(self)
        self.lastResponse = None

    def generate_response(self, input_str : str, args):

        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }
        
        post_data = {
            "inputs": input_str,
            "seed": 1,
            "parameters": {
                "sample_or_greedy": "sample",
                "max_new_tokens": args["max_new_tokens"]
            },
            "last_response": self.lastResponse,
        }

        x = requests.post("https://opengptx.dfki.de/generate", headers=headers, data = json.dumps(post_data))
        self.lastResponse = x.json()["output_text"]
        return (x.json()["output_text"])
