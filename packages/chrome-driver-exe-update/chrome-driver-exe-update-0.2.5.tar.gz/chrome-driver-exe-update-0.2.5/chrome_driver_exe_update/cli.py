import argparse

from chrome_driver_exe_update import ChromeDriver


def main():
    parser = argparse.ArgumentParser(description="Create a webdriver to handle a browser and download files.")
    parser.add_argument("--downloads_path", help="Path to downloads files.")
    parser.add_argument("--headless", action="store_true", help="Run with headless mode.")
    parser.add_argument("--driver_executable", help="Path to chromedriver executable.")
    parser.add_argument("--software_dir", help="Path to directory where chrome will be installed.")
    parser.add_argument("--downloads_type", help="Type of file to be downloaded.")
    args = parser.parse_args()

    chrome_driver = ChromeDriver(
        downloads_path=args.downloads_path or "temp",
        headless=args.headless,
        driver_executable=args.driver_executable,
        software_dir=args.software_dir or "_software",
        downloads_type=args.downloads_type,
    )
    chrome_driver.create_driver()


if __name__ == "__main__":
    main()
