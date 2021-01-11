# -*- coding: utf-8 -*-
"""
Created on 2021/1/10 14:35

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

__version__ = '0.1'

setup(
    name="tinyCrawl",
    version=__version__,
    description='Very easy and tiny crawling framework, support multithread processing.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Irvinfaith',
    author_email='waxiguan00@hotmail.com',
    url="https://github.com/Irvinfaith/tinyCrawl",
    license='MIT',
    platforms='python 3.6',
    python_requires='>=3.6,<4',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Operating System :: OS Independent',
    ],
)
