import argparse
import logging

from llm import llm_registry
from llm.http_api import start_api

class Application:

    def __init__(self):
        self.args = None

    def get_args(self):

        if self.args is None:
            parser = argparse.ArgumentParser(prog="LLM Tools")
            parser.add_argument('--llm', type=str, required=True, help="Specify which LLM you want to load.")
            parser.add_argument('--huggingface_model', type=str, required=False, help="When llm=transformers, specify the huggingface model here.")
            parser.add_argument('--input_str', type=str, help="Specify input document. For mode=oneshot.")
            parser.add_argument('--mode', default="oneshot", choices=["http_api", "oneshot"])
            parser.add_argument('--log_level', default="warning", choices=["info", "warning"])
            parser.add_argument('--api_url', type=str)
            parser.add_argument('--port', type=int, default=5000)
            
            self.args = parser.parse_args()
        return self.args

    def init_logging(self, args):
        level = logging.WARNING
        if args.log_level == "info":
            level = logging.INFO

        logging.basicConfig(format='%(levelname)s:%(message)s', level=level)

def run_console():

    app = Application()
    args = app.get_args()
    app.init_logging(args)

    logging.info("loading llm " + args.llm)

    if args.llm not in llm_registry.get_llms():
        raise Exception("Unknown LLM " + args.llm)
    
    llm = llm_registry.load_llm(app, args.llm)

    if args.mode == "oneshot":
        if args.input_str is None:
            raise Exception("Parameter input_str not set")
        response = llm.generate_response(args.input_str)
        logging.info("Get response " + response)
        print(response)
    elif args.mode == "http_api":
        start_api(llm, args)

if __name__ == "__main__":
    run_console()