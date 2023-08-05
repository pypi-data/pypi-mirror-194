from configparser import ConfigParser

from sdfspu.ini_config import parse_ini_file


def test_parse_ini_file_():
    config = parse_ini_file("test.ini")
    assert isinstance(config, ConfigParser)
    assert config.get("abc123", "a") == "one"
    assert config.getint("abc123", "b") == 2
    assert config.getfloat("abc123", "c") == 3.14


def test_parse_ini_file_fallback():
    fallback = {"abc123": {"a": "one", "b": 2, "c": 3.14}}
    config = parse_ini_file("nope.ini", or_dict=fallback)
    assert isinstance(config, ConfigParser)
    assert config.get("abc123", "a") == "one"
    assert config.getint("abc123", "b") == 2
    assert config.getfloat("abc123", "c") == 3.14


def test_parse_ini_file_and_dict():
    additional = {"abc123": {"d": 1, "c": "333.444", "z": 0}}
    config = parse_ini_file("test.ini", and_dict=additional)
    assert isinstance(config, ConfigParser)
    assert config.get("abc123", "a") == "one"
    assert config.getint("abc123", "b") == 2
    assert config.getfloat("abc123", "c") == 333.444  # overwritten value
    assert config.getboolean("abc123", "d")
    assert not config.getboolean("abc123", "z")
