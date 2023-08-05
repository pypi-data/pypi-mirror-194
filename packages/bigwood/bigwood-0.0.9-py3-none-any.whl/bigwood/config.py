"""Useful utilities for config stuff
"""
import configparser
from pathlib import Path


def get_config(path: Path):

    config = configparser.ConfigParser()
    config.read(path)
    return config


