#!/usr/bin/env python
from setuptools import setup

# Given a version number MAJOR.MINOR.PATCH, increment the:
# MAJOR version when you make incompatible API changes
# MINOR version when you add functionality in a backwards compatible manner
# PATCH version when you make backwards compatible bug fixes


setup(
    name='kadota',
    version='1.0.2',
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