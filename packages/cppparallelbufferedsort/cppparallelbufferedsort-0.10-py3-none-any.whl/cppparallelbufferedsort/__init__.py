from .cppparallelbufferedsortmodule import cpp_parallel_buffered_sort
import numpy as np
def parallel_buffered_sort(a):
    a2 = a.size
    a3 = np.zeros_like(a)
    a4 = a3.size
    cpp_parallel_buffered_sort(a, a2, a3, a4)
    return a3