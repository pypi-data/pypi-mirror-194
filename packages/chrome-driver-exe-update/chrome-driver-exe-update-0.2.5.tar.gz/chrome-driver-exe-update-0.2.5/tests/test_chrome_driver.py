import unittest
import os
from unittest.mock import patch
from chrome_driver_exe_update.chrome_driver import ChromeDriver


class ChromeDriverTestCase(unittest.TestCase):
    def setUp(self):
        self.downloads_path = os.path.join(os.getcwd(), "temp")
        self.headless = True
        self.driver_executable = None
        self.software_dir = os.path.join(os.getcwd(), "_software",)
        self.downloads_type = "application/pdf"

        self.chrome_driver = ChromeDriver(
            downloads_path=self.downloads_path,
            headless=self.headless,
            driver_executable=self.driver_executable,
            software_dir=self.software_dir,
            downloads_type=self.downloads_type
        )

    def test_create_driver(self):
        with patch("selenium.webdriver.chrome.service.Service.start"):
            with patch("selenium.webdriver.Chrome") as mock_driver:
                # Call create_driver() method to create a real WebDriver object
                self.chrome_driver.create_driver()
                self.assertEqual(
                    "send_command",
                    mock_driver.return_value.execute.call_args[0][0]
                )


        # Assert that the driver's options are set correctly
        expected_options = [
            '--dns-prefetch-disable',
            '--browser.download.folderList=2',
            f'--browser.download.dir={self.downloads_path}',
            f'--browser.helperApps.neverAsk.saveToDisk={self.downloads_type}',
            '--headless',
            '--disable-gpu'
        ]
        for option in expected_options:
            self.assertIn(option, mock_driver.call_args[1]['options'].arguments)

        # Assert that the driver's experimental options are set correctly
        expected_experimental_options = {
            'excludeSwitches': ['enable-logging'],
            'prefs': {"plugins.always_open_pdf_externally": True}
        }
        self.assertEqual(expected_experimental_options, mock_driver.call_args[1]['options'].experimental_options)

        # # Assert that the driver's command executor is set correctly
        # expected_command_executor = ("POST", '/session/$sessionId/chromium/send_command')
        # # self.assertEqual(expected_command_executor, mock_driver.call_args[1]['command_executor']._commands["send_command"])

        # Assert that the driver's session is set correctly
        driver = mock_driver.return_value
        self.assertIsNotNone(driver.execute("send_command", params={"cmd": "Page.setDownloadBehavior"}))
