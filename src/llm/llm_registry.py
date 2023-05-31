from llm.wrapper.llm_wrapper import LLMWrapper, DummyLLM, OpenAIDavinci, RemoteHTTPLLM

def load_llama(size):
    from llm.wrapper.llama.llama_wrapper import LLamaWrapper
    return LLamaWrapper()

def load_automodel(app):
    from llm.wrapper.automodel.automodel_wrapper import AutoModelWrapper
    return AutoModelWrapper(app)

def load_t5(app):
    from llm.wrapper.t5.t5_wrapper import T5Wrapper
    return T5Wrapper(app)

def init_remote_http_llm(app):
    if "api_url" not in app.get_args():
        raise Exception("--url parameter not set.")
    return RemoteHTTPLLM(app.get_args().api_url)

llm_registry = {
    "openai_davinci": lambda app : OpenAIDavinci(),
    "dummy_llm": lambda app : DummyLLM(),
    "llama-7b": lambda app : load_llama("7B"),
    "automodel": lambda app : load_automodel(app),
    "t5": lambda app : load_t5(app),
    "http": init_remote_http_llm
}

def load_llm(app, llm_name):
    return llm_registry[llm_name](app)

def get_llms():
    return llm_registry.keys()