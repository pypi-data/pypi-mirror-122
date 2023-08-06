from setuptools import setup
from setuptools import find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='Youtube_scrapper',
    version='0.0.3',
    description='A tool for extracting youtube video details',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/VBamgbaye/Web_Scraping_Project.git',
    author='Victor Bamgbaye',
    author_email='bamgbayev@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['selenium', 'pandas']
)
