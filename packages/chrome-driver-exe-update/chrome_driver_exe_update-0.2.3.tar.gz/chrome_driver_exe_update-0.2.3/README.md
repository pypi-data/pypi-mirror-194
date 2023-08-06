# Webdriver Package

The Chrome Driver Downloader is a Python module that simplifies the process
of creating a Selenium webdriver for the Google Chrome browser.

It checks if the current version of the Chrome browser is compatible
with the installed chromedriver and downloads a new version if necessary.

## Installation

To install the module, run the following command:

```shell
pip install chrome-driver-exe-update
```

## Usage

The module can be used with command line arguments or by importing it
in a Python script. Here are some examples:

### Command line

To run the module from the command line, use the following command:

```shell
python -m chrome-driver-exe-update -d [DOWNLOADS_PATH] -h [HEADLESS] -e [DRIVER_EXECUTABLE_PATH] -s [SOFTWARE_DIR] -t [DOWNLOADS_TYPE]
```

where:

* [DOWNLOADS_PATH] is the path where downloaded files will be saved
* [HEADLESS] is a boolean indicating whether to run the browser in headless mode
* [DRIVER_EXECUTABLE_PATH] is the path to the chromedriver executable (optional)
* [SOFTWARE_DIR] is the path where Chrome is installed (optional)
* [DOWNLOADS_TYPE] is the type of file to be downloaded (optional)

### Python script

To use the module in a Python script, import it and create an instance
of the ChromeDriver class, passing the required arguments:

```python
from src.chrome_driver import ChromeDriver

downloads_path = "[DOWNLOADS_PATH]"
headless = "[HEADLESS]"
driver_executable = "[DRIVER_EXECUTABLE_PATH]"
software_dir = "[SOFTWARE_DIR]"
downloads_type = "[DOWNLOADS_TYPE]"

driver = ChromeDriver(downloads_path, headless, driver_executable, software_dir, downloads_type)
driver.create_driver()
```

## License

The Chrome Driver Downloader is released under the MIT License.
See LICENSE for more information.

Change Log
----------

* 0.1.0
    * Change: Start production.
* 0.1.9
    * Change: Download a new version of chromedriver if current oudated.
* 0.2.0
    * Change: Refactor code to add upload package to pypi

Meta
----

Author: [Frederico Gago](https://www.linkedin.com/in/frederico-gago-5849281aa/)

E-Mail: fredyisaac@gmail.com

&copy; 2022 by Frederico Gago
