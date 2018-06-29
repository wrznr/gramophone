# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gramophone',
    version='0.0.1',
    description='grapheme-phoneme conversion and related stuff',
    long_description=readme,
    author='Kay-Michael Würzner, Bryan Jurish',
    author_email='wuerzner@bbaw.de, jurish@bbaw.de',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
    ],
    entry_points={
          'console_scripts': [
              'gramophone=gramophone.scripts.gramophone:cli',
              'gramophone-server=gramophone.scripts.gramophone_server:cli',
          ]
    },
)
