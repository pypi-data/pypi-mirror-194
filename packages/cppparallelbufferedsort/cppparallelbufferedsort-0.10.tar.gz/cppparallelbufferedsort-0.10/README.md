# parallel_buffered_sort from C++ for Python (Windows)

## pip install cppparallelbufferedsort

#### Microsoft Visual C++ Redistributable is necessary
https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170



```python
from cppparallelbufferedsort import parallel_buffered_sort
import numpy as np

a1 = np.random.randint(0, 2000000, 1000000)
a2 = parallel_buffered_sort(a1)
fl = a1 / 3
f2 = parallel_buffered_sort(fl)
# Out[6]:
# array([0.00000000e+00, 6.66666667e-01, 1.33333333e+00, ...,
#        6.66664333e+05, 6.66664667e+05, 6.66664667e+05])

# %timeit parallel_buffered_sort(fl)
# 18.4 ms ± 128 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# %timeit np.sort(fl)
# 61.5 ms ± 90.1 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)



```