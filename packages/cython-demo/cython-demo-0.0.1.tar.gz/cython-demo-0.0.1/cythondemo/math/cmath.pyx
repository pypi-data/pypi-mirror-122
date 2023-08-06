# distutils:language=c++
# cython:language_level=3

from libc.math cimport sqrt

cpdef double heron(double a, double b, double c):
    cdef double p;
    p = (a + b + c) / 2.0
    return sqrt(p * (p - a) * (p - b) * (p - c))
