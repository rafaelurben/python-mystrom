import logging

from pystrom.console import MyStromCommandParser

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    MyStromCommandParser()
