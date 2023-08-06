import json
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin

from requests import HTTPError

from pwbm_api_utils.constants import ENV_DATA
from pwbm_api_utils.helpers.pbar import pbar
from pwbm_api_utils.helpers.session import get_session
from .base import CommandBase


def push_map_tag(session, env, map_name):
    try:
        logging.debug(f'Creating tag {map_name}')
        r = session.post(
            url=f'tags/',
            json={
                'name': 'Metric',
                'value': map_name,
            },
        )
        r.raise_for_status()
        tag_id = r.json()['id']

        logging.debug(f'Adding tag to buckets')
        r = session.put(
            url=f'tags/{tag_id}',
            json={
                'buckets': ENV_DATA[env]['metric_tag_buckets'],
            },
        )
        r.raise_for_status()

        return tag_id

    except HTTPError as err:
        logging.error('Error occured creating tag', exc_info=True)
        raise


def load_series(session, series_id):
    try:
        logging.debug(f'Loading series {series_id}')
        r = session.get(
            url=f'series/{series_id}',
            params={
                'format': 'json',
            }
        )
        r.raise_for_status()
        return r.json()['info']['tags']
    except HTTPError as err:
        logging.error('Error occurred fetching series', exc_info=True)
        raise


def add_series_to_map(session, map_id, series_id):
    series_tags = load_series(session, series_id)
    series_tag_ids = [t['id'] for t in series_tags]

    if map_id in series_tag_ids:
        logging.debug(f'Series {series_id} is already part of the map {map_id}')
        return

    logging.debug(f'Adding map tag to series {series_id}')
    series_tag_ids.append(map_id)
    r = session.put(
        url=f'series/{series_id}',
        json={
            'tags': series_tag_ids,
        },
    )
    r.raise_for_status()

    return series_id


def push_map(session, env, map_file):
    with map_file.open() as in_f:
        map_data = json.load(in_f)
    map_id = push_map_tag(session, env, map_data['name'])

    logging.info(f'Name: {map_data["name"]}')
    logging.info(f'ID: {map_id}')
    logging.info('UI link: %s', urljoin(ENV_DATA[env]['ui_prefix'], f'map/{map_id}'))
    logging.info('API link: %s', urljoin(ENV_DATA[env]['api_prefix'], f'metrics/{map_id}'))
    logging.info(f'Origin: {map_file}')
    logging.info(f'Series count: {len(map_data["series"])}')

    series_ids = [s['id'] for s in map_data['series']]
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(add_series_to_map, session, map_id, s_id) for s_id in series_ids]
        for future in pbar(futures, desc='Map progress'):
            try:
                future.result()
            except Exception:
                raise


def collect_map_paths(paths: list) -> tuple:
    res_paths = set()
    for path in paths:
        if path.is_dir():
            res_paths.update(path.glob('**/*.json'))
        else:
            res_paths.add(path)
    return tuple(res_paths)


def maps_path(path: str):
    path = Path(path)
    if not path.exists():
        print(path, 'Path does not exist')
        raise ValueError('Path does not exist')
    if path.is_file() and path.suffix != '.json':
        print(path, 'Incorrect file name')
        raise ValueError('Incorrect file name')
    return path


class Command(CommandBase):
    name = 'push'
    help = 'Push generated maps to the API'
    description = 'Push generated maps to the API'

    @classmethod
    def configure_cli(cls, parser):
        parser.add_argument(
            'path', type=maps_path, nargs='+',
            help='path to the previously generated map file(s)',
        )

    @classmethod
    def run(cls, args):
        map_file_paths = collect_map_paths(args.path)
        logging.info(f'Pushing maps ({len(map_file_paths)} in total)')
        session = get_session(args.environment, args.user, args.password)
        for map_file in pbar(map_file_paths, desc='Overall progress'):
            push_map(session, args.environment, map_file)
