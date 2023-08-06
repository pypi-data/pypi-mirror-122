from setuptools import setup, find_packages

import os

VERSION = '0.0.8'
DESCRIPTION = "Flipkart Web Scrapping Package"

from os import path
this_directory = path.abspath(path.dirname(__file__))

#with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()
long_description = "This Package extracts the data from flipkart"


#Setting up
setup(
    name="flipkart_scrapping",
    version=VERSION,
    author="Rajesh Kumar Patnala",
    author_email="patnala04@gmail.com",
    url='https://github.com/rajeshpatnala/flipkart-web-scrapping',
    description=DESCRIPTION,
    packages=find_packages() +
             find_packages(".") + 
             find_packages(where="mongo_operations") +
             find_packages(where="extract_details") + 
             find_packages(where="modules") + 
             find_packages(where="file_oper") + 
             find_packages(where="settings.py"),
    install_requires=['bs4', 'pymongo', 'bson'],
    keywords=['python', 'web scrapping', 'flipkart', 'beautiful soup', 'data extraction'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
),
