from configparser import ConfigParser

import logging
from typing import Optional

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


def parse_ini_file(
    path_to_ini_file, or_dict: Optional[dict] = None, and_dict: Optional[dict] = None
) -> ConfigParser:
    """
    load config from a .ini file (or a dict, or both)
    :param path_to_ini_file: path to a .ini file
    :param or_dict: fallback dict to read instead of .ini in case of FileNotFoundError
    :param and_dict: additional dict to read as well as the (.ini or fallback)
    :return: ConfigParser object
    """
    config = ConfigParser()
    try:
        config.read_file(open(path_to_ini_file))
    except FileNotFoundError as e:
        log.warning(f"Error loading '{path_to_ini_file}'")
        log.error(e)
        if or_dict:
            config.read_dict(or_dict)
    if and_dict:
        config.read_dict(and_dict)
    return config
