"""
utilities shared by bdrc_utils
"""
import argparse
from pathlib import Path
from typing import AnyStr


def reallypath(what_path: AnyStr) -> Path:
    """
    Resolves everything about the path
    :param what_path: Pathlike object
    :return: fully resolved path
    """
    from os import path

    # jimk #499: detect non-file paths and don't expand
    if what_path is None:
        return None
    # Regex more elegant, but need fastway to say UNCs must be at beginning
    if what_path.find('://') > 0 or what_path.startswith('//') or what_path.startswith('\\'):
        return what_path

    return path.realpath(path.expandvars(path.expanduser(what_path)))

