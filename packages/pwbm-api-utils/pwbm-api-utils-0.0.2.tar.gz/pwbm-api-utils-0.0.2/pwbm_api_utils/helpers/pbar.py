from functools import partial

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm


def shorten_text(text):
    if text and len(text) > 50:
        pass


tqdm_params = {
    # 'ncols': 80,
    'miniters': 1,
    'bar_format': '> {l_bar}{bar}| [{elapsed}]',
}

pbar = partial(tqdm, **tqdm_params)
pbar.redirect_logging = logging_redirect_tqdm
