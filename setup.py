#!/usr/bin/env python
# -*- coding: utf-8 -*-
# yapf:disable
from __future__ import absolute_import, division, print_function

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()


base_requirements = [
    'requests',
]


requirements = base_requirements


setup(
    name='gh-release',
    version='0.1.2',
    description="Small cli to upload GH releases",
    long_description=readme,
    author="Antoine Legrand",
    author_email='2t.antoine@gmail.com',
    url='https://github.com/ant31/gh-release',
    packages=[
        'ghrelease',
    ],
    scripts=['bin/ghrelease'],
    package_dir={'ghrelease': 'ghrelease'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords=['github'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ])
