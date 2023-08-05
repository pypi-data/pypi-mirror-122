#!/usr/bin/env python3
"""
This module provides the number class Rat (for rational), a drop-in replacement for the fractions.Fractions class,
based on gmpy.mpq
"""

from setuptools import setup

classifiers = """
"""

setup(name='mpqfractions',
      version='0.1',
      description='Drop-in replacement for fractions.Fraction, using gmpy', 
      long_description=__doc__,
      classifiers=list(filter(None, classifiers.split('\n'))),
      author='Eduardo Moguillansky',
      author_email='eduardo.moguillansky@gmail.com',
      py_modules=['mpqfractions'],
      url="https://github.com/gesellkammer/mpqfractions"
)


