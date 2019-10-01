#!/usr/bin/env python3
from setuptools import setup, find_packages

_dev = {'develop':
        ['pylint', 'pytest', 'pytest-cov', 'pytest-asyncio',
         'asynctest', 'aioresponses']}

setup(
    name='qb',
    version='0.1.0',
    description='This demo script provide functionality to copy data from on API endpoint to anothers',
    author='Dimitar Dimitrov',
    author_email='targolini@gmail.com',
    url='https://github.com/dimddev/qb',
    packages=find_packages(),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - 5',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD3 License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7.4',
    ],
    install_requires=[
        'trio-click==7.0.3',
        'aiohttp==3.6.1',
    ],

    scripts=['qb.py'],
    extras_require=_dev
)
