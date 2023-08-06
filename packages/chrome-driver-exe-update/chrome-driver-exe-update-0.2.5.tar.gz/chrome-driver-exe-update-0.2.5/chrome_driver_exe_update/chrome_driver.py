"""Module that ill create the webdriver.

It downloads files too.
"""

import os
import glob
import zipfile
import io
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, SessionNotCreatedException

from win32com.client import *
import requests
from bs4 import BeautifulSoup
import re


logger = logging.getLogger(__name__)


class ChromeDriver:
    """Create the Webdriver.

    In case that the webdriver is outdated checks the version of chrome
    and then downloads the chromedriver corresponding to the new version.

    Args:
        downloads_path (str): Path to donwloads files.
        headless (bool): Run with window or not.
        downloads_type (str, optional): Type of file to be downloaded.
            Defaults to None.

    Attributes:
        downloads_path (str): Path to donwloads files.
        headless (bool): Run with window or not.
        downloads_type (str, optional): Type of file to be downloaded.
            Defaults to None.
        driver_executable_path (str, optional): Path to chromedriver.
            Defaults to None.
    """

    def __init__(self, downloads_path, headless, driver_executable,
                 software_dir, downloads_type=None):
        self.downloads_path = downloads_path
        self.headless = headless
        self.downloads_type = downloads_type
        self.driver_executable_path = driver_executable if driver_executable else ""
        if not os.path.exists(self.driver_executable_path):
            self.software_path = software_dir
            self.driver_executable_path = self.download_new_version()
        self.driver = None

    def create_driver(self):
        """Creates driver with all the options and start.

        If error, **outdated** start process to download new chromedriver.

        Returns:
            Webdriver: Driver to handle browser.

        Raises:
            SessionNotCreatedException: When driver is outdated.
        """

        options = webdriver.ChromeOptions()
        # Cross-Origin domain disable resolve IP address
        options.add_argument('--dns-prefetch-disable')

        # Change download default to temp
        options.add_argument("--browser.download.folderList=2")
        options.add_argument("--browser.download.dir=" + self.downloads_path)

        # Download without asking
        if self.downloads_type is not None:
            options.add_argument("--browser.helperApps.neverAsk.saveToDisk=" + self.downloads_type)

        # Disable a visible UI shell.
        if self.headless:
            options.add_argument("--headless")

        # Improvement speed and needed for windows headless driver
        options.add_argument("--disable-gpu")

        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        options.add_experimental_option('prefs', {"plugins.always_open_pdf_externally": True})

        timeout = 30
        while True:
            try:
                service = ChromeService(self.driver_executable_path)
                driver = webdriver.Chrome(
                    service=service,
                    options=options
                )
            except SessionNotCreatedException as e:
                logger.info("Webdriver is outdated, starting download new one...")
                self.driver_executable_path = self.download_new_version()
                timeout -= 1
                if timeout < 0:
                    raise
            except Exception as err:
                logger.critical(f"Driver got an error starting: {err}")
                raise
            else:
                break

        # Allows Chrome to download when in headless mode
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {
            'cmd': 'Page.setDownloadBehavior',
            'params': {'behavior': 'allow', 'downloadPath': self.downloads_path}
        }
        driver.execute("send_command", params)

        self.driver = driver

    @staticmethod
    def find_chrome_exe(search_file):
        """Find in pc driver the Chrome exe.

        Args:
            search_file (str): file to search.

        Returns:
            path: Path to Chrome exe.

        Raises:
            FileNotFoundError: Doesn't find chrome.exe in **C:** drive.
        """

        if search_file.startswith("chrome"):
            common_chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if os.path.isfile(common_chrome_path):
                return common_chrome_path
        else:
            file = None
            for file in glob.glob(f"C:\\Pro*\\**\\{search_file}", recursive=True):
                return file
            if not file:
                logger.critical("Cannot find Google Chrome in the root directory.")
                raise FileNotFoundError("Cannot find Google Chrome, please be sure"
                                        " to install it with the root directory"
                                        r" 'C:\Program Files\Google\Chrome\Application'")

    def check_version_of_chrome(self):
        """Checks version of current Chrome browser installed

        Returns:
            str: Version of the current Chrome.
        """

        chrome_exe = self.find_chrome_exe("chrome.exe")
        file_info = Dispatch("Scripting.FileSystemObject")
        version = file_info.GetFileVersion(chrome_exe)
        return version

    @staticmethod
    def find_last_version_link(curr_version):
        """Gets the link of the right version of the chromedriver.exe.

        Args:
            curr_version (str): Current Version of the Chrome Browser installed.

        Returns:
            str: Link to new version of the chromedriver.exe.
        """

        response = requests.get("https://chromedriver.chromium.org/downloads")

        pattern_href = rf"https://chromedriver.storage.googleapis.com/index.html\?path=({curr_version}.[\d\.]+)/"
        pattern_version = re.compile(r"path=([\d\.]+)/")
        pattern_last_version = r"(\d+)\.(\d+)\.(\d+)\.(\d+)"

        parser = BeautifulSoup(response.content, "html.parser")
        # Find all links in the page
        links = parser.find_all(href=re.compile(pattern_href))
        links = [link.get("href") for link in links]
        # Finds the versions in the links
        versions = list(map(lambda v: pattern_version.search(v).group(1), links))
        # Finds the lastest version 2.5.3 > 2.2.5
        latest_version = max(versions, key=lambda l: [int(v) for v in re.search(pattern_last_version, l).groups()])
        return latest_version

    def download_new_version(self):
        """Donwloads the new version of the chromedriver.exe

        Returns:
            str: path of the new chromedriver.exe.
        """

        logger.debug("Download webdriver.")

        chrome_version = self.check_version_of_chrome()
        target_version = chrome_version.split('.')[0]
        latest_version = self.find_last_version_link(target_version)

        logger.debug(f"Browser version: {chrome_version}\nUrl_new_version: {latest_version}")

        base_url = "https://chromedriver.storage.googleapis.com/"
        zip_endpoint = "chromedriver_win32.zip"
        response = requests.get(base_url + latest_version + "/" + zip_endpoint)
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(self.software_path)
        return os.path.join(self.software_path, "chromedriver.exe")

    @staticmethod
    def is_downloaded(download_path, current_files):
        """Checks if the download is done by seeing with dir has
        a new number of files.

        Args:
            download_path (str): Path to download dirs.
            current_files (int): Number of files in `path_download`
                before download.

        Returns:
            bool: Exists a new file in `path_download`.
        """

        if len(os.listdir(download_path)) == current_files:
            return False
        else:
            return True

    @staticmethod
    def change_name_last_file(name_file, download_path):
        """Change last file that appear in dir to a new name.

        Args:
            name_file (str): File new name.
            download_path (str): Path to download file.

        Returns:
            str: New named file in absolute path.
        """
        abs_new_name_file = os.path.join(download_path, name_file)
        logger.info(f"Changing last downloaded file to: {abs_new_name_file}")

        files = os.listdir(download_path)
        paths = [os.path.join(download_path, basename) for basename in files]

        # Last file in dir
        old_file = max(paths, key=os.path.getctime)

        os.rename(old_file, abs_new_name_file)
        return abs_new_name_file

    @staticmethod
    def download_file_from_url(driver, url, name_file, download_path):
        """Downloads to `downloads_path` the url file and gives a name.

        Args:
            driver (any): Driver that controls the browser.
            url (str): Url to download file.
            name_file (str): The name to rename file downloaded.
            download_path (str): Path to download file.

        Returns:
            str: New file absolute path.

        Raises:
            TimeoutException: File doesn't download in time.
        """
        logger.info(f"Starting download file: {url}")
        current_n_files = len(os.listdir(download_path))
        try:
            driver.get(url)
            WebDriverWait(driver, 30, 2).until(
                lambda d: ChromeDriver.is_downloaded(download_path, current_n_files)
            )
        except TimeoutException:
            logger.critical(f"Cannot download file, url: {url}")
            return False
        else:
            new_file_path = ChromeDriver.change_name_last_file(name_file, download_path)
            return new_file_path

    def __repr__(self):
        rep = (
            f"ChromeDriver(driver_executable_path={self.driver_executable_path}, "
            f"headless={self.headless} "
            f"downloads_path={self.downloads_path} "
            f"downloads_type={self.downloads_type})"
        )
        return rep
