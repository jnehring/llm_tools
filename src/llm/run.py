import argparse
import logging

from llm import llm_registry
from llm.util import init_logging
from llm.http_api import start_api

def run_console():

    parser = argparse.ArgumentParser(prog="LLM Tools")
    parser.add_argument('--llm', type=str, required=True, help="Specify which LLM you want to load.")
    parser.add_argument('--input_str', type=str, help="Specify input document. For mode=oneshot.")
    parser.add_argument('--mode', default="oneshot", choices=["http_api", "oneshot"])
    parser.add_argument('--log_level', default="warning", choices=["info", "warning"])

    args = parser.parse_args()

    init_logging(args)

    logging.info("loading llm " + args.llm)

    if args.llm not in llm_registry.get_llms():
        raise Exception("Unknown LLM " + args.llm)
    
    llm = llm_registry.load_llm(args.llm)

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