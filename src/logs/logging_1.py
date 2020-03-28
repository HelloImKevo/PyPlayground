#!/usr/bin/python

import logging
import logginglib


def main():
    my_logger = logging.getLogger('Log Tester')
    # Filemode 'w' will overwrite existing file contents!
    logging.basicConfig(filename='example_logs.log', filemode='w', level=logging.DEBUG)
    my_logger.setLevel(logging.INFO)

    my_logger.log(logging.DEBUG, "Debug test")
    my_logger.log(logging.INFO, "Info test")
    my_logger.log(logging.CRITICAL, "Critical test")

    logginglib.do_something()

    my_logger.debug("Debug test")
    my_logger.info("Info test")
    my_logger.critical("Critical test")

    my_logger.info("Some other random log message")


if __name__ == '__main__':
    main()
