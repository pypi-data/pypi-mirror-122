import json
import logging
import string
import shutil
import time
from collections import defaultdict, Counter
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urljoin
from uuid import UUID

from requests import HTTPError

from pwbm_api_utils.constants import ENV_DATA
from pwbm_api_utils.helpers.pbar import pbar
from pwbm_api_utils.helpers.session import get_session
from .base import CommandBase


def load_row_tree(session, table_id, row_id='root'):
    table_info = None
    table_rows = []
    try:
        page_num, page_count = 0, 1
        with pbar(total=100, desc='Loading table') as p_bar:
            while page_count != page_num:
                r = session.get(
                    url=f'tables/{table_id}/rows/{row_id}/children',
                    params={
                        'descendants': 'all',
                        'include_values': False,
                        'page_size': 1,
                        'page': page_num,
                    }
                )
                r.raise_for_status()
                data = r.json()
                page_num, page_count = data['page_num'], data['page_count']
                table_info = data['info']
                table_rows.extend(data['data_items'])
                p_bar.update(100 // page_count)
    except HTTPError as err:
        logging.error('Error occured fetching table info', exc_info=True)
        raise

    return {
        'info': table_info,
        'data_items': table_rows,
    }


def traverse_row_tree(row, results: dict, env_data: dict, prefix: tuple = ()) -> dict:
    """Recursive traversal of a table row hierarchy."""
    child_prefix = (*prefix, row['line_attributes']['row_id'])
    if results is None:
        results = defaultdict(list)
    if row['info'] and row['info']['tags']:
        for tag in row['info']['tags']:
            if tag['name'] == 'FIPS':
                results['/'.join(prefix if tag['value'] != '00' else child_prefix)].append({
                    'id': row['info']['id'],
                    'name': row['info']['name'],
                    'fips': tag['value'],
                    'api_url': urljoin(env_data['api_prefix'], f'series/{row["info"]["id"]}'),
                    'ui_url': urljoin(env_data['ui_prefix'], f'series/{row["info"]["id"]}'),
                    'tags': [
                        {
                            'id': t['id'],
                            'name': t['name'],
                            'value': t['value'],
                        } for t in row['info']['tags']
                    ],
                })
                break
    for child_row in row['descendants']:
        traverse_row_tree(child_row, results, env_data, child_prefix)
    return results


def generate_map_name(series: list) -> str:
    map_name = series[0]['name']
    for series_name in (sn for s in series if (sn := s['name'])):
        matching_name_parts = SequenceMatcher(a=map_name, b=series_name).get_matching_blocks()[:-1]
        map_name = ''.join(map_name[np.a:np.a + np.size] for np in matching_name_parts)
    return map_name.strip(string.punctuation + string.whitespace)


def generate_map_warnings(env_data, series: list) -> list:
    warnings = []

    fips = []
    existing_metrics = set()
    for series_data in series:
        for tag in series_data['tags']:
            if tag['name'] == 'FIPS':
                fips.append(tag['value'])
            elif tag['name'] == 'Metric':
                existing_metrics.add((tag['id'], tag['value']))
    duplicate_fips = set(item for item, count in Counter(fips).items() if count > 1)
    unique_fips = tuple(set(fips))

    if existing_metrics:
        maps_info = []
        for map_id, map_name in existing_metrics:
            ui_link = urljoin(env_data['ui_prefix'], f'map/{map_id}')
            api_link = urljoin(env_data['api_prefix'], f'metrics/{map_id}')
            maps_info.append('\n'.join((
                f'  Name: {map_name}',
                f'  ID: {map_id}',
                f'  UI link: {ui_link}',
                f'  API link: {api_link}',
            )))
        warnings.append('Some series are already used in maps:\n' + '\n  ---\n'.join(maps_info))
    if duplicate_fips:
        warnings.append(f'Map contains duplicate FIPS: {", ".join(duplicate_fips)}')
    if len(unique_fips) == 1:
        warnings.append(f'Map contains data for a single FIPS: {unique_fips[0]}')

    return warnings


def generate_maps(env_data, table_data):
    series_groups = defaultdict(list)
    for row in table_data['data_items']:
        traverse_row_tree(row, series_groups, env_data)

    if not series_groups:
        return

    maps_dir = Path(f'maps_{datetime.utcnow().isoformat(timespec="seconds")}')
    for (group_prefix, group_series) in pbar(series_groups.items(), desc='Overall progress'):
        map_file_relative_path = Path(f'table_{table_data["info"]["id"]}').joinpath(
            *map((lambda s: f'row_{s}'), group_prefix.split('/')),
            f'map_{hex(abs(hash(group_prefix)))[2:10]}.json'
        )

        logging.info(f'Generating {map_file_relative_path}')
        with pbar(total=1, desc='Map progress') as fake_pbar:
            map_definition = {
                'name': generate_map_name(group_series),
                'generated': {
                    'at': datetime.utcnow().isoformat(),
                    'from': {
                        'table': {
                            'id': table_data['info']['id'],
                            'api_url': urljoin(env_data['api_prefix'], f'tables/{table_data["info"]["id"]}'),
                            'ui_url': urljoin(env_data['ui_prefix'], f'tables/{table_data["info"]["id"]}'),
                            'intable_location': group_prefix,
                        },
                    },
                },
                'warnings': generate_map_warnings(env_data, group_series),
                'series': sorted(group_series, key=lambda s: s['fips']),
            }

            for message in map_definition['warnings']:
                logging.warning(message)

            map_file = maps_dir / map_file_relative_path
            map_file.parent.mkdir(parents=True, exist_ok=True)
            with map_file.open('w') as out_f:
                json.dump(map_definition, out_f, indent=2)

            fake_pbar.update(1)


def str_uuid(id_: str):
    return str(UUID(id_))


def table_row_id(id_: str):
    if id_ != 'root':
        return str_uuid(id_)
    return id_


class Command(CommandBase):
    name = 'generate'
    help = 'Generate maps from DB data'
    description = (
        'Generate maps from DB data. '
        'Generated maps are saved locally for manual adjustments'
    )

    @classmethod
    def configure_cli(cls, parser):
        subparsers = parser.add_subparsers(title='source', dest='source')
        generate_from_table_cmd = subparsers.add_parser(
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

    @classmethod
    def run(cls, args):
        logging.info('Generating maps')
        session = get_session(args.environment, args.user, args.password)
        row_tree = load_row_tree(session, args.table, args.row)
        generate_maps(ENV_DATA[args.environment], row_tree)
