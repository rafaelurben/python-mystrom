import logging

from pystrom.console import MyStromCommandParser


def main() -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    MyStromCommandParser()


if __name__ == "__main__":
    main()
