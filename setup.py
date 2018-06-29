from setuptools import setup, find_packages
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('tayne/tayne.py').read(),
    re.M
    ).group(1)

setup(
    name='tayne',
    author='James Campbell',
    author_email='james@jamescampbell.us',
    version=version,
    license='GPLv3',
    description = 'Identify and rate bots on social media.',
    packages=['tayne'],
    py_modules=['tayne'],
    keywords = ['tayne', 'data-analysis', 'robots', 'rating', 'turing-test'],
    classifiers = ["Programming Language :: Python :: 3 :: Only"],
    install_requires=[
        'argparse',
        'pandas',
        'pprint',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'tayne = tayne.tayne:main',
        ],
        },
    url = 'https://github.com/jamesacampbell/tayne',
    download_url = 'https://github.com/jamesacampbell/tayne/archive/{}.tar.gz'.format(version)
)