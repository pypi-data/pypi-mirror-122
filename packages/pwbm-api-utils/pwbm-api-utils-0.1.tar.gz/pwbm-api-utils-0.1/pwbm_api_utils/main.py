#!/usr/bin/env python3
import argparse
import sys

from .cmds import commands
from .constants import APIEnvs
from .helpers.pbar import pbar
from .helpers.logs import configure_logging


def _parse_args():
    parser = argparse.ArgumentParser(
        prog='pwbm-api-utils',
        description='Set of administrative tools for PWBM API',
    )
    parser.add_argument(
        '-e', '--env', required=True, type=APIEnvs, choices=tuple(e.value for e in APIEnvs), dest='environment',
        help='API environment to use'
    )
    parser.add_argument(
        '-u', '--user', required=True,
    )
    parser.add_argument(
        '-p', '--password', required=True, metavar='PSWD',
    )
    parser.add_argument(
        '-v', '--verbose', action="store_true",
        help='print debug info',
    )

    cmd_parsers = parser.add_subparsers(title='commands', dest='cmd')
    for subcommand in commands:
        subcommand.register_subparser(cmd_parsers)

    return parser.parse_args()


def main():
    args = _parse_args()
    configure_logging(args.verbose)
    with pbar.redirect_logging():
        return args.cmd_callable(args)


if __name__ == '__main__':
    sys.exit(main())
