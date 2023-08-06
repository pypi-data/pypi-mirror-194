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
    name='de-awsUtils',
    version='0.0.1',
    url='https://github.com/delvira13/_awsUtils',
    packages=['awsUtils'],
    install_requires=requires,
    license='LICENSE.txt',
    python_requires=">= 3.10"
)