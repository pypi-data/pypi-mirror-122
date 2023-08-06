"""
da-lab2-test

A test package for data analysis homework
"""

__version__ = "0.0.6"
__author__ = 'Dmitriy Kolchin'
__credits__ = 'ITMO University'

import numpy.version

np_ver = numpy.version.version
print(np_ver)
if np_ver != '1.17.2':
    raise ImportError("Numpy version should be 1.17.2")
