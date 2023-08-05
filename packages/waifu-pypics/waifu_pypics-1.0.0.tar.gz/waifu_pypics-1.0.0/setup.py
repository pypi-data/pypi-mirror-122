#!/usr/bin/env python

from io import open
from setuptools import setup


"""
Author: Reidy
"""


version = '1.0.0'

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='waifu_pypics',
    version=version,

    author='Reidy',

    description='Waifu-Pics Api Pyrhon Wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/JeanSkripchenko/Waifu-Pypics',
    download_url='https://github.com/JeanSkripchenko/Waifu-Pypics/archive/refs/heads/master.zip',

    packages=['waifu_pypics'],
    install_requires=['aiohttp', 'requests', 'asyncio']
)
