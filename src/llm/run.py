import configargparse
import logging

from llm import llm_registry
from llm.http_api import start_api

class Application:

    def __init__(self):
        self.args = None

    def get_args(self):

        if self.args is None:

            parser = configargparse.ArgumentParser(prog="LLM Tools")
            parser.add_argument('--wrapper', type=str, required=True, help="Specify which LLM you want to load.")
            parser.add_argument('--model', type=str, required=False, help="Specify the model here.")

            parser.add_argument('--input_str', type=str, help="Specify input document. For mode=oneshot.")
            parser.add_argument('--mode', default="http_api", choices=["http_api", "oneshot"])
            parser.add_argument('--log_level', default="warning", choices=["info", "warning"])
            parser.add_argument('--api_url', type=str)
            parser.add_argument('--port', type=int, default=5000, env_var='LLM_TOOLS_PORT')
            parser.add_argument('--log_all_queries', action="store_true", help="log all queries to queries.txt")
            
            self.args = parser.parse_args()
        return self.args

    def init_logging(self, args):
        level = logging.WARNING
        if args.log_level == "info":
            level = logging.INFO

        logging.basicConfig(format='%(levelname)s:%(message)s', level=level, filename="log.txt")

def run_console():

    app = Application()
    args = app.get_args()
    app.init_logging(args)

    logging.info("loading llm " + args.wrapper)

    if args.wrapper not in llm_registry.get_llms():
        raise Exception("Unknown LLM " + args.wrapper)
    
    llm = llm_registry.load_llm(app, args.wrapper)
    print("llm is", llm)

    if args.mode == "oneshot":
        if args.input_str is None:
            raise Exception("Parameter input_str not set")

        response = llm.generate_response(args.input_str, {})

        # example to test cond_log_prob
        # in_str = "What color is the sky? Answer: blue\nWhat color is grass? Answer:"
        # targets = ["red", "blue", "green"]
        # response = llm.cond_log_prob(in_str, targets, {})
        logging.info("Get response " + str(response))
        print(type(response), type(response[0]))
        print(response)
    elif args.mode == "http_api":
        start_api(llm, args)

if __name__ == "__main__":
    run_console()