#!/usr/bin/env python

from distutils.core import setup
setup(
    name = 'kpoints-convergence',
    version = '0.1.0',
    description = 'Automatically determines k-point mesh for desired total energy convergence.',
    author = 'Brian A Day',
    author_email = '22bday@gmail.com',
    url = 'https://github.com/birdday/rewotes/birdday',
    packages = ['kpoints-convergence'],
    install_requires=[
        'numpy',
    ],
    extras_require={'plotting': ['matplotlib']}
)
