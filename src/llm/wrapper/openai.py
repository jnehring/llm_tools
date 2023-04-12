import os
import openai

from llm.wrapper.llm_wrapper import LLMWrapper

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
