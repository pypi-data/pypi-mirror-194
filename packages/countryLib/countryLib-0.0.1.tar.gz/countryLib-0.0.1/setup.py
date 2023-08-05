from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Country library'
LONG_DESCRIPTION = 'A package that allows to get country information like official name, population and so on... ' \
                   'To use "from country.countryLib import Country"'

# Setting up
setup(
    name="countryLib",
    version=VERSION,
    author="Abraham",
    author_email="ibrohimjon.ismoilov.007@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['httpx'],
    keywords=['python', 'country', 'information', 'country information', 'population', 'area of countries',
              'country borders', 'map of countries', 'continent', 'world'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
