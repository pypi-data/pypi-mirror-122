# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import numpy.ma


def numpy_diag(diag):
    return numpy.ma.diag(diag)


def numpy_randint(min_value, max_value, num):
    return np.random.randint(min_value, max_value, num)
