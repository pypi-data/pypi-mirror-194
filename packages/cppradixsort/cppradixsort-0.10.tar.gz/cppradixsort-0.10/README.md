# parallel_radixsort from C++ for Python (Windows)

## pip install cppradixsort

#### Microsoft Visual C++ Redistributable is necessary
https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170



```python
from cppradixsort import parallel_radixsort

import numpy as np

a1 = np.random.randint(0, 2000000, 1000000)
a2 = parallel_radixsort(a1)

# a1
# Out[3]: array([ 173641, 1852805, 1959843, ..., 1094448,  430953, 1021449])
# a2
# Out[4]: array([      0,       0,      13, ..., 1999996, 1999996, 1999997])
# %timeit parallel_radixsort(a1)
# 4.96 ms ± 32.6 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# %timeit np.sort(a1,kind='stable')
# 63.8 ms ± 72.9 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)


```