from setuptools import setup
from setuptools import find_packages

setup(
    name='Youtube_scrapper',
    version='0.0.1',
    description='A tool for extracting youtube video details',
    url='https://github.com/VBamgbaye/Web_Scraping_Project.git',
    author='Victor Bamgbaye',
    author_email='bamgbayev@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['selenium', 'pandas']
)
