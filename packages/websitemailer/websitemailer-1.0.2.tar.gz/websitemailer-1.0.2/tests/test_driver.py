"""Test suite for websitemailer.driver"""
import sys
from distutils.spawn import find_executable
from loguru import logger
from pathlib import Path

from websitemailer.driver import get_version_via_com, get_chrome_driver, get_chrome_driver_version
from websitemailer.screenshots import take_screenshot

__author__ = "Brian Seel"
__copyright__ = "Brian Seel"
__license__ = "MIT"


def test_get_version_via_com():
    """Test for get_version_via_com"""
    if sys.platform == 'win32':
        assert get_version_via_com(Path(__file__).parent / 'testfiles' / 'chrome.exe') == 92
    else:
        path = list(Path('/tmp').glob('chrome-*/chrome'))[0]
        logger.info(f'Using binary {path}')
        assert isinstance(get_version_via_com(path), int)
        assert get_version_via_com(path) >= 92
    assert get_version_via_com(Path(__file__).parent / 'pathdoesnotexist') == -1


def test_get_chrome_driver(tmp_path_factory):
    """Test for get_chrome_driver"""
    temp_dir = tmp_path_factory.mktemp('driver')
    driver_path = get_chrome_driver(94, Path(temp_dir))
    driver_version = get_chrome_driver_version(94)
    assert driver_path.exists()
    assert driver_path in (temp_dir / driver_version).glob('chromedriver*')
    assert len(list(temp_dir.glob('*'))) == 1

    # do it again and it should not download again
    assert not get_chrome_driver(94, Path(temp_dir))
    assert len(list(temp_dir.glob('*'))) == 1

    # do it again and make sure it goes in a temp directory
    driver_path = get_chrome_driver(94)
    assert driver_path
    assert driver_path.exists()

    # specify path
    temp_file = tmp_path_factory.mktemp('ss_test') / 'screenshot.png'
    screenshot = take_screenshot('http://www.google.com', driver_path, temp_file)
    assert screenshot.exists()
    assert screenshot.stat().st_size > 10000

    # don't specify path
    screenshot = take_screenshot('http://www.google.com', driver_path)
    assert screenshot.exists()
    assert screenshot.stat().st_size > 10000


def test_get_chrome_driver_version():
    assert get_chrome_driver_version()
