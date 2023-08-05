"""Tests for the `files` functions"""
import pytest
from pathlib import Path
from files 



def test_trim_path_to_folder():
    """Check that we get the bottom folder we
    are expecting"""

    path = Path("/home/user/dev/project/boo/bar")
    result = trim_path_to_folder(path, "project")
    assert Path("/home/user/dev/project") == result


def test_trim_path_to_folder_raise():
    """Check that we do something sensible if
    and invalid folder is passed"""

    path = Path("/home/user/dev/project/boo/bar")
    with pytest.raises(ValueError):
        trim_path_to_folder(path, "deadbeef")

