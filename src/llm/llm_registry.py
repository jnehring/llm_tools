from llm.wrapper.llm_wrapper import LLMWrapper
from llm.wrapper.dummy_llm import DummyLLM
from llm.wrapper.openai import OpenAIDavinci

llm_registry = {
    "openai_davinci": lambda : OpenAIDavinci(),
    "dummy_llm": lambda : DummyLLM()
}

def load_llm(name):
    return llm_registry[name]()

def get_llms():
    return llm_registry.keys()