#!/usr/bin/env python

from distutils.core import setup
setup(
    name = 'kpoint',
    version = '0.1.0',
    description = 'Automatically determines k-point mesh for desired total energy convergence using Mat3ra workflows.',
    author = 'Brian A Day',
    author_email = '22bday@gmail.com',
    url = 'https://github.com/birdday/rewotes/birdday',
    packages = ['kpoint'],
    install_requires=[
        'exabyte-api-client',
        'urllib'
    ]
)
