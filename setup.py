# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='skabvm',
    version='0.1.0',
    description='A simple KVM provisioning tool',
    long_description=readme,
    author='Pierguido Lambri',
    author_email='pierg75@yahoo.it',
    url='https://github.com/pierg75/skabvm',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

