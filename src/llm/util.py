import logging

def init_logging(args):

    level = logging.WARNING
    if args.log_level == "info":
        level = logging.INFO

    logging.basicConfig(format='%(levelname)s:%(message)s', level=level)
