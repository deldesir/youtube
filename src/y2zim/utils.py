import json
import re
from slugify import slugify


def get_id_type(id):
    """
    Given a YouTube ID, returns its type (either 'playlist', 'channel_id', or 'channel_user').
    """
    # if id is Nonetype, return None
    if id is None:
        return None
    # if id is a string, check if it's a playlist, channel, or user
    if isinstance(id, str):
        # First, check if it's a playlist ID
        if re.match(r'^PL[-_a-zA-Z0-9]{16,}$', id):
            return 'playlist'
        if re.match(r'^UC[-_a-zA-Z0-9]{22,}$', id):
            return 'channel'
        if re.match(r'^[a-zA-Z0-9]+$', id):
            return 'user'
        return None
    # if id is a list, check if it's a list of playlist IDs
    if isinstance(id, list):
        if all([re.match(r'^PL[-_a-zA-Z0-9]{16,}$', i) for i in id]):
            return 'playlist'
        return None


def check_file_type(file):
    if file.endswith('.csv'):
        return 'csv'    
    elif file.endswith('.txt'):
        return 'txt'
    else:
        return None


def get_slug(text, js_safe=True):
    """slug from text to build URL parts"""
    if js_safe:
        return slugify(text, regex_pattern=r"[^-a-z0-9_]+").replace("-", "_")
    return slugify(text)


def clean_text(text):
    """cleaned-down version of text as Youtube is very permissive with descriptions"""
    return text.strip().replace("\n", " ").replace("\r", " ")


def save_json(cache_dir, key, data):
    """save JSON collection to path"""
    with open(cache_dir.joinpath(f"{key}.json"), "w") as fp:
        json.dump(data, fp, indent=4)


def load_json(cache_dir, key):
    """load JSON collection from path or None"""
    fname = cache_dir.joinpath(f"{key}.json")
    if not fname.exists():
        return None
    try:
        with open(fname, "r") as fp:
            return json.load(fp)
    except Exception:
        return None