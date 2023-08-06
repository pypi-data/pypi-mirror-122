from setuptools import setup
from setuptools import find_packages

setup(
    name = 'HristoScraper',
    version = '0.0.8',
    description = 'This is a car price scraper package',
    url = 'https://github.com/xristo01/Data_Engineering_Project',
    author = 'Hristo Petkov',
    license = 'MIT',
    packages = find_packages(),
    install_requires = ['pandas', 'selenium', 'numpy', 'sqlalchemy'])