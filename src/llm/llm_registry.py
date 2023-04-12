from llm.wrapper.llm_wrapper import LLMWrapper
from llm.wrapper.dummy_llm import DummyLLM
from llm.wrapper.openai import OpenAIDavinci

def load_llama(size):
    from llm.wrapper.llama.llama_wrapper import LLamaWrapper
    return LLamaWrapper()

llm_registry = {
    "openai_davinci": lambda : OpenAIDavinci(),
    "dummy_llm": lambda : DummyLLM(),
    "llama-7b": lambda : load_llama("7B")
}

def load_llm(name):
    return llm_registry[name]()

def get_llms():
    return llm_registry.keys()