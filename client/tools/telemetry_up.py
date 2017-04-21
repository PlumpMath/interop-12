#!/usr/bin/env python
#make sure you set python path in terminal
#USNA SUAS interop client
#This is the async telemetry client

from __future__ import print_function
import argparse
import datetime
import getpass
import logging
import pprint
import sys
import time

from interop import AsyncClient
from proxy_mavlink import proxy_mavlink

logger = logging.getLogger(__name__)


def mavlink(args, client):
    proxy_mavlink(args.device, client)


def main():
    #initialize logging
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')

    #parse command line args.
    parser = argparse.ArgumentParser(description='Async interop CLI.')
    parser.add_argument('--url',
                        required=True,
                        help='URL for server.')
    parser.add_argument('--username',
                        required=True,
                        help='Username for server login.')
    parser.add_argument('--password',help='Password for server login.')

    subparsers = parser.add_subparsers(help='Sub-command help.')

    subparser = subparsers.add_parser(
         'mavlink',
         help='''Receive MAVLink GLOBAL_POSITION_INT packets and
 forward as telemetry to interop server.''')
    subparser.set_defaults(func=mavlink)
    subparser.add_argument(
         '--device',
         type=str,
         help='pymavlink device name to read from. E.g. tcp:localhost:8080.')

    # Parse args, get password
    args = parser.parse_args()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass('Interoperability Password: ')

    # Create client and dispatch subcommand.
    client = AsyncClient(args.url, args.username, password)
    args.func(args, client)

if __name__ == '__main__':
    main()
