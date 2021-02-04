# Rafael Urben, 2021
#
# https://github.com/rafaelurben/python-mystrom

import sys
import argparse

from pystrom.search import MyStromSearch
from pystrom.utils import log

class MyStromCommandParser(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='[PyStrom] Control MyStrom devices',
            usage="""pystrom <command> [args]
            
Possible commands:
  search      Search MyStrom devices in your local network
            """)
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            log('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def search(self):
        parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        parser.add_argument('--live', action='store_true', help="Keep connection open until manually stopped.")
        args = parser.parse_args(sys.argv[2:])
        if args.live:
            MyStromSearch.searchlive()
        else:
            MyStromSearch.searchall()
