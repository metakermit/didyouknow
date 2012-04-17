'''
Created on 14. 3. 2012.

@author: kermit
'''
from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "foc-forecaster",
    version = "0.1",
    packages = find_packages(),
    install_requires = ['matplotlib>=1.0.1',
                        'xlrd>=0.6.1'],
    zip_safe = True,
    
    # metadata for upload to PyPI
    author = "Drazen Lucanin",
    author_email = "kermit666@gmail.com",
    url = "http://pypi.python.org/pypi/foc-forecaster",
    long_description=read('README')
)
