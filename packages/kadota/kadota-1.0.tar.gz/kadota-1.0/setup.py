#!/usr/bin/env python
from setuptools import setup

setup(
    name='kadota',
    version='1.0',
    description='Tools for working with Figma programmatically',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Isaac Ronald Ward',
    author_email='isaacronaldward@gmail.com',
    license='MIT',
    packages=['kadota'],
    include_package_data=True,
    install_requires=[line.strip() for line in open("requirements.txt").readlines()]
)