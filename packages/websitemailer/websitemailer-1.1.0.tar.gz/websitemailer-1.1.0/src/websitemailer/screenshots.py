"""Takes a screenshot of a webpage"""
from pathlib import Path
from tempfile import NamedTemporaryFile

from loguru import logger
from selenium import webdriver  # type: ignore
from selenium.webdriver.chrome.options import Options  # type: ignore


def take_screenshot(url, driver_path, dest_file: Path = None, delay: int = 0) -> Path:
    """
    Take a screenshot with Selenium
    :param url: URL of the page to screenshot
    :param driver_path: Where the Chrome driver was saved
    :param dest_file: Full path to save the screenshot. If None, then its put in a temporary directory
    :param delay: Number of seconds to delay before taking the screenshot; good for long loading pages
    :return: The location the file was saved
    """
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(driver_path, options=options)
    driver.get(url)
    driver.implicitly_wait(delay)
    if not dest_file:
        with NamedTemporaryFile(suffix='.png') as temp_path:
            dest_file = Path(temp_path.name)
    logger.info(f'Taking screenshot of {url}, saving it to {dest_file} with driver {driver_path}')
    driver.save_screenshot(str(dest_file))
    driver.close()

    return dest_file
