# -*- coding: utf-8 -*-
"""
Created on 2021/1/10 14:35

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
from setuptools import setup, find_packages


setup(
    name="tinyCrawl",
    version="0.1",
    description='Very easy and tiny crawling framework, support multithread processing.',
    author='Irvinfaith',
    author_email='irvinfaith@hotmail.com',
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
