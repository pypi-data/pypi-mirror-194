from .cppradixsortmodule import cpp_parallel_radixsort
import numpy as np
def parallel_radixsort(a):
    a2 = a.size
    a3 = np.zeros_like(a)
    a4 = a3.size
    cpp_parallel_radixsort(a, a2, a3, a4)
    return a3