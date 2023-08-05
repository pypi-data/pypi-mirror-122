#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from uuid import UUID

import pwbm_api_utils.cmds as cmds
from .constants import APIEnvs
from .helpers.pbar import pbar
from .helpers.logs import configure_logging


def str_uuid(id_: str):
    return str(UUID(id_))


def table_row_id(id_: str):
    if id_ != 'root':
        return str_uuid(id_)
    return id_


def maps_path(path: str):
    path = Path(path)
    if not path.exists():
        print(path, 'Path does not exist')
        raise ValueError('Path does not exist')
    if path.is_file() and path.suffix != '.json':
        print(path, 'Incorrect file name')
        raise ValueError('Incorrect file name')
    return path


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

    generate_cmd = cmd_parsers.add_parser(
        name='generate',
        description=(
            'Generate maps from DB data. '
            'Generated maps are saved locally for manual adjustments'
        ),
        help='Generate maps from DB data',
    )
    generate_cmd.set_defaults(cmd_callable=cmds.generate)
    generate_cmd_parsers = generate_cmd.add_subparsers(title='source', dest='source')

    generate_from_table_cmd = generate_cmd_parsers.add_parser(
        name='table',
        description='Generate maps using table hierarchy',
        help='Generate maps using table hierarchy',
    )
    generate_from_table_cmd.add_argument(
        'table', type=str_uuid, metavar='TABLE_ID',
    )
    generate_from_table_cmd.add_argument(
        '--row', type=table_row_id, metavar='ROW_ID', default='root',
        help=(
            'ID of the specific table row for hierarchy traversal. '
            'Only descendants of this row would be used for map generation'
        ),
    )

    push_cmd = cmd_parsers.add_parser(
        name='push',
        description='Push generated maps to the API',
        help='Push generated maps to the API',
    )
    push_cmd.set_defaults(cmd_callable=cmds.push)
    push_cmd.add_argument(
        'path', type=maps_path, nargs='+',
        help='path to the previously generated map file(s)'
    )

    return parser.parse_args()


def main():
    args = _parse_args()
    configure_logging(args.verbose)
    with pbar.redirect_logging():
        return args.cmd_callable(args)


if __name__ == '__main__':
    sys.exit(main())
