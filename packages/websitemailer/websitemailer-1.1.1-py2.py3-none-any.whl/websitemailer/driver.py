"""Handles everything related to the Chrome and Selenium drivers"""
import os
import sys
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Optional

import pefile  # type: ignore
import requests
from loguru import logger

__author__ = "Brian Seel"
__copyright__ = "Brian Seel"
__license__ = "MIT"


def get_version_via_com(filename: Path):
    """
    Gets the major version of Chrome that is installed
    :param filename: Path to the Chrome binary
    :return: Major version of the Chrome binary
    """
    if not os.path.exists(filename):
        logger.error(f'Chrome binary {filename} does not exist')
        return -1

    if sys.platform == 'win32':
        pe_file = pefile.PE(filename)
        verinfo = pe_file.VS_FIXEDFILEINFO[0]
        prodver = (verinfo.ProductVersionMS >> 16,
                   verinfo.ProductVersionMS & 0xFFFF,
                   verinfo.ProductVersionLS >> 16,
                   verinfo.ProductVersionLS & 0xFFFF)
        version = prodver[0]
    else:
        # expected return is like 'Chromium 96.0.4660.0' or 'Google Chrome 94.0.4606.71'
        version_str = os.popen(f'{filename} --version').read()  # nosec
        logger.info(version_str)
        if version_str.startswith('Google Chrome'):
            version_str = version_str.split(' ')[2]
        elif version_str.startswith('Chromium'):
            version_str = version_str.split(' ')[1]
        else:
            raise AssertionError(f'Unexpected version string: {version_str}')
        version = int(version_str.split('.')[0])

    logger.info(f'Chrome version is {version}')
    return version


def get_chrome_driver_version(version: Optional[int] = None) -> str:
    """
    Get the full version of the chrome driver
    :param version: The major version to look up. If none is provided, it gets the latest version
    :return: The version of the chrome driver
    """
    ver_str = f'_{version}' if version else ''
    url = f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE{ver_str}'

    logger.info(f'Getting {url}')
    resp = requests.get(url)
    return resp.text


def get_chrome_driver(version: int, dest_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Downloads the Chrome driver from Selenium to a local directory
    :param version: Major version number of the Chrome binary installed
    :param dest_dir: Directory to download the
    :return:
    """
    driver_version = get_chrome_driver_version(version)
    logger.info(f'Getting Chrome driver version {version} ({driver_version}) and downloading to {dest_dir}')

    if dest_dir is None:
        dest_dir = Path(tempfile.TemporaryDirectory().name)  # pylint:disable=consider-using-with
        logger.info(f'Dest dir set to {dest_dir}')

    if os.path.exists(dest_dir / driver_version):
        logger.info(f'Chrome driver version {driver_version} already exists in {dest_dir}')
        return None

    plat = 'win32' if sys.platform == 'win32' else 'linux64'

    url = f'https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_{plat}.zip'
    logger.info(f'Pulling zipfile: {url}')
    driver_zip = BytesIO(requests.get(url).content)
    with zipfile.ZipFile(driver_zip, 'r') as zip_file:
        zip_file.extractall(dest_dir / driver_version)

    for file in (dest_dir / driver_version).glob('chromedriver*'):
        if sys.platform != 'linux64':
            os.chmod(file, 0o0755)  # nosec
        return file
    return None
