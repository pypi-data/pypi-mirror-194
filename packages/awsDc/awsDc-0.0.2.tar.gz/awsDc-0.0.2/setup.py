#!/usr/bin/env python

"""
distutils/setuptools install script.
"""
from setuptools import setup

requires = [
    'boto3>=1.26.63',
    'pandas>=1.5.3'
]

setup(
    name='awsDc',
    version='0.0.2',
    url='https://github.com/delvira13/_awsDc',
    scripts=[],
    packages=['_awsDc'],
    install_requires=requires,
    license='LICENSE.txt',
    python_requires=">= 3.7"
)