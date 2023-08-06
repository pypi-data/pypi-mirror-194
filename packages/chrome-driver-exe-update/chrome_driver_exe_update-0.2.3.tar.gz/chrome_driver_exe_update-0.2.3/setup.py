from setuptools import find_packages
from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    readme = f.read()

setup(
    name="chrome_driver_exe_update",
    version="0.2.3",
    license='MIT',
    description=readme,
    long_description_content_type="text/markdown",
    author="Frederico Gago",
    author_email='fredyisaac@gmail.com',
    packages=find_packages(),
    url='https://github.com/FredericoIsaac/chrome_driver',
    keywords='chrome driver selenium',
    install_requires=[
        "selenium==4.1.3",
        "beautifulsoup4==4.10.0",
        "pywin32==303",
        "requests==2.27.1",
        "setuptools==67.4.0"
    ],
    entry_points={
        "console_scripts": [
            "chrome-driver-exe-update=src.cli:main",
        ],
    },
)
