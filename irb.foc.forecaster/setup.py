'''
Created on 24. 9. 2012.

@author: kermit
'''

from distutils.core import setup

setup(
    name='Dracula',
    version='0.1.0',
    author=u"Dražen Lučanin",
    author_email='kermit666@gmail.com',
    packages=['dracula', 'dracula.test'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    license='http://www.gnu.org/licenses/gpl-3.0.html',
    description='A cache-enabled wrapper for some public APIs (currently, only the World Bank).',
    long_description=open('dracula/README.md').read(),
    install_requires = ['matplotlib>=1.0.1',
                        'xlrd>=0.6.1'],
    zip_safe = True,
)