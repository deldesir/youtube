import json

import logging
import pathlib

from zimscraperlib.logging import getLogger

ROOT_DIR = pathlib.Path(__file__).parent
NAME = ROOT_DIR.name

with open(ROOT_DIR.joinpath("VERSION"), "r") as fh:
    VERSION = fh.read().strip()

SCRAPER = f"{NAME} {VERSION}"

# Youtube uses some non-standard language codes
YOUTUBE_LANG_MAP = {
    "iw": "he",  # Hebrew
    "es-419": "es",  # Spanish
    "zh-Hans-CN": "zh-cn",  # Chinese
    "zh-Hant-TW": "zh-tw",  # Chinese
    "zh-Hant-HK": "zh-hk",  # Chinese
    "zh-Hans-SG": "zh-sg",  # Chinese
    "mo": "ro",  # Romanian
    "sh": "srp",  # Serbian
}

logger = getLogger(NAME, level=logging.DEBUG, file='/output_dir/y2zim.log')


with open("/usr/local/etc/ytable/config.json") as f:
    config = json.load(f)
API_KEY = config["API_KEY"]
    

class Youtube:
    def __init__(self):
        self.build_dir = None
        self.cache_dir = None
        self.api_key = None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


YOUTUBE = Youtube()