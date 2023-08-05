import sys
import ctypes
from numpy.ctypeslib import ndpointer
import configparser
from flexible_partial import FlexiblePartialOwnName
import numpy as np
import os


def get_file(f):
    return os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), f))


def cpp_parallel_radixsort(
    v0,
    v1,
    v2,
    v3,
):

    if v0.dtype == np.byte and v2.dtype == np.byte:
        v0np = np.require(v0, np.byte, ["ALIGNED", "C_CONTIGUOUS"])
        v0po = v0np.ctypes.data_as(ctypes.POINTER(ctypes.c_byte))
        v1po = int(v1)
        v2np = np.require(v2, np.byte, ["ALIGNED", "C_CONTIGUOUS"])
        v2po = v2np.ctypes.data_as(ctypes.POINTER(ctypes.c_byte))
        v3po = int(v3)
        c_functions.bb_cpp_parallel_radixsort_signed_char_size_t_signed_char_size_t(
            v0po,
            v1po,
            v2po,
            v3po,
        )
        return
    if v0.dtype == np.ubyte and v2.dtype == np.ubyte:
        v0np = np.require(v0, np.ubyte, ["ALIGNED", "C_CONTIGUOUS"])
        v0po = v0np.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
        v1po = int(v1)
        v2np = np.require(v2, np.ubyte, ["ALIGNED", "C_CONTIGUOUS"])
        v2po = v2np.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
        v3po = int(v3)
        c_functions.bb_cpp_parallel_radixsort_unsigned_char_size_t_unsigned_char_size_t(
            v0po,
            v1po,
            v2po,
            v3po,
        )
        return
    if v0.dtype == np.short and v2.dtype == np.short:
        v0np = np.require(v0, np.short, ["ALIGNED", "C_CONTIGUOUS"])
        v0po = v0np.ctypes.data_as(ctypes.POINTER(ctypes.c_short))
        v1po = int(v1)
        v2np = np.require(v2, np.short, ["ALIGNED", "C_CONTIGUOUS"])
        v2po = v2np.ctypes.data_as(ctypes.POINTER(ctypes.c_short))
        v3po = int(v3)
        c_functions.bb_cpp_parallel_radixsort_short_size_t_short_size_t(
            v0po,
            v1po,
            v2po,
            v3po,
        )
        return
    if v0.dtype == np.ushort and v2.dtype == np.ushort:
        v0np = np.require(v0, np.ushort, ["ALIGNED", "C_CONTIGUOUS"])
        v0po = v0np.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))
        v1po = int(v1)
        v2np = np.require(v2, np.ushort, ["ALIGNED", "C_CONTIGUOUS"])
        v2po = v2np.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort))
        v3po = int(v3)
        c_functions.bb_cpp_parallel_radixsort_unsigned_short_size_t_unsigned_short_size_t(
            v0po,
            v1po,
            v2po,
            v3po,
        )
        return
    if v0.dtype == np.intc and v2.dtype == np.intc:
        v0np = np.require(v0, np.intc, ["ALIGNED", "C_CONTIGUOUS"])
        v0po = v0np.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        v1po = int(v1)
        v2np = np.require(v2, np.intc, ["ALIGNED", "C_CONTIGUOUS"])
        v2po = v2np.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        v3po = int(v3)
        c_functions.bb_cpp_parallel_radixsort_int_size_t_int_size_t(
            v0po,
            v1po,
            v2po,
            v3po,
        )
        return
    if v0.dtype == np.uintc and v2.dtype == np.uintc:
        v0np = np.require(v0, np.uintc, ["ALIGNED", "C_CONTIGUOUS"])
        v0po = v0np.ctypes.data_as(ctypes.POINTER(ctypes.c_uint))
        v1po = int(v1)
        v2np = np.require(v2, np.uintc, ["ALIGNED", "C_CONTIGUOUS"])
        v2po = v2np.ctypes.data_as(ctypes.POINTER(ctypes.c_uint))
        v3po = int(v3)
        c_functions.bb_cpp_parallel_radixsort_unsigned_int_size_t_unsigned_int_size_t(
            v0po,
            v1po,
            v2po,
            v3po,
        )
        return
    if v0.dtype == np.int_ and v2.dtype == np.int_:
        v0np = np.require(v0, np.int_, ["ALIGNED", "C_CONTIGUOUS"])
        v0po = v0np.ctypes.data_as(ctypes.POINTER(ctypes.c_long))
        v1po = int(v1)
        v2np = np.require(v2, np.int_, ["ALIGNED", "C_CONTIGUOUS"])
        v2po = v2np.ctypes.data_as(ctypes.POINTER(ctypes.c_long))
        v3po = int(v3)
        c_functions.bb_cpp_parallel_radixsort_long_size_t_long_size_t(
            v0po,
            v1po,
            v2po,
            v3po,
        )
        return
    if v0.dtype == np.uint and v2.dtype == np.uint:
        v0np = np.require(v0, np.uint, ["ALIGNED", "C_CONTIGUOUS"])
        v0po = v0np.ctypes.data_as(ctypes.POINTER(ctypes.c_ulong))
        v1po = int(v1)
        v2np = np.require(v2, np.uint, ["ALIGNED", "C_CONTIGUOUS"])
        v2po = v2np.ctypes.data_as(ctypes.POINTER(ctypes.c_ulong))
        v3po = int(v3)
        c_functions.bb_cpp_parallel_radixsort_unsigned_long_size_t_unsigned_long_size_t(
            v0po,
            v1po,
            v2po,
            v3po,
        )
        return
    if v0.dtype == np.longlong and v2.dtype == np.longlong:
        v0np = np.require(v0, np.longlong, ["ALIGNED", "C_CONTIGUOUS"])
        v0po = v0np.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong))
        v1po = int(v1)
        v2np = np.require(v2, np.longlong, ["ALIGNED", "C_CONTIGUOUS"])
        v2po = v2np.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong))
        v3po = int(v3)
        c_functions.bb_cpp_parallel_radixsort_long_long_size_t_long_long_size_t(
            v0po,
            v1po,
            v2po,
            v3po,
        )
        return
    if v0.dtype == np.ulonglong and v2.dtype == np.ulonglong:
        v0np = np.require(v0, np.ulonglong, ["ALIGNED", "C_CONTIGUOUS"])
        v0po = v0np.ctypes.data_as(ctypes.POINTER(ctypes.c_ulonglong))
        v1po = int(v1)
        v2np = np.require(v2, np.ulonglong, ["ALIGNED", "C_CONTIGUOUS"])
        v2po = v2np.ctypes.data_as(ctypes.POINTER(ctypes.c_ulonglong))
        v3po = int(v3)
        c_functions.bb_cpp_parallel_radixsort_unsigned_long_long_size_t_unsigned_long_long_size_t(
            v0po,
            v1po,
            v2po,
            v3po,
        )
        return


allargtypes = [
    (
        "cpp_parallel_radixsort_signed_char_size_t_signed_char_size_t",
        r"""ctypes.POINTER( ctypes.c_byte), ctypes.c_size_t,ctypes.POINTER( ctypes.c_byte), ctypes.c_size_t,""",
        "bb_",
        "aa_",
        None,
        [
            ctypes.POINTER(ctypes.c_byte),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_byte),
            ctypes.c_size_t,
        ],
    ),
    (
        "cpp_parallel_radixsort_unsigned_char_size_t_unsigned_char_size_t",
        r"""ctypes.POINTER( ctypes.c_ubyte), ctypes.c_size_t,ctypes.POINTER( ctypes.c_ubyte), ctypes.c_size_t,""",
        "bb_",
        "aa_",
        None,
        [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_size_t,
        ],
    ),
    (
        "cpp_parallel_radixsort_short_size_t_short_size_t",
        r"""ctypes.POINTER( ctypes.c_short), ctypes.c_size_t,ctypes.POINTER( ctypes.c_short), ctypes.c_size_t,""",
        "bb_",
        "aa_",
        None,
        [
            ctypes.POINTER(ctypes.c_short),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_short),
            ctypes.c_size_t,
        ],
    ),
    (
        "cpp_parallel_radixsort_unsigned_short_size_t_unsigned_short_size_t",
        r"""ctypes.POINTER( ctypes.c_ushort), ctypes.c_size_t,ctypes.POINTER( ctypes.c_ushort), ctypes.c_size_t,""",
        "bb_",
        "aa_",
        None,
        [
            ctypes.POINTER(ctypes.c_ushort),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ushort),
            ctypes.c_size_t,
        ],
    ),
    (
        "cpp_parallel_radixsort_int_size_t_int_size_t",
        r"""ctypes.POINTER( ctypes.c_int), ctypes.c_size_t,ctypes.POINTER( ctypes.c_int), ctypes.c_size_t,""",
        "bb_",
        "aa_",
        None,
        [
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_size_t,
        ],
    ),
    (
        "cpp_parallel_radixsort_unsigned_int_size_t_unsigned_int_size_t",
        r"""ctypes.POINTER( ctypes.c_uint), ctypes.c_size_t,ctypes.POINTER( ctypes.c_uint), ctypes.c_size_t,""",
        "bb_",
        "aa_",
        None,
        [
            ctypes.POINTER(ctypes.c_uint),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_uint),
            ctypes.c_size_t,
        ],
    ),
    (
        "cpp_parallel_radixsort_long_size_t_long_size_t",
        r"""ctypes.POINTER( ctypes.c_long), ctypes.c_size_t,ctypes.POINTER( ctypes.c_long), ctypes.c_size_t,""",
        "bb_",
        "aa_",
        None,
        [
            ctypes.POINTER(ctypes.c_long),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_long),
            ctypes.c_size_t,
        ],
    ),
    (
        "cpp_parallel_radixsort_unsigned_long_size_t_unsigned_long_size_t",
        r"""ctypes.POINTER( ctypes.c_ulong), ctypes.c_size_t,ctypes.POINTER( ctypes.c_ulong), ctypes.c_size_t,""",
        "bb_",
        "aa_",
        None,
        [
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.c_size_t,
        ],
    ),
    (
        "cpp_parallel_radixsort_long_long_size_t_long_long_size_t",
        r"""ctypes.POINTER( ctypes.c_longlong), ctypes.c_size_t,ctypes.POINTER( ctypes.c_longlong), ctypes.c_size_t,""",
        "bb_",
        "aa_",
        None,
        [
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.c_size_t,
        ],
    ),
    (
        "cpp_parallel_radixsort_unsigned_long_long_size_t_unsigned_long_long_size_t",
        r"""ctypes.POINTER( ctypes.c_ulonglong), ctypes.c_size_t,ctypes.POINTER( ctypes.c_ulonglong), ctypes.c_size_t,""",
        "bb_",
        "aa_",
        None,
        [
            ctypes.POINTER(ctypes.c_ulonglong),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ulonglong),
            ctypes.c_size_t,
        ],
    ),
]
dllpath = get_file(f=r"cppradixsort.dll")
cfgfile = get_file(f=r"cppradixsort.ini")
lib = ctypes.CDLL(dllpath)
confignew = configparser.ConfigParser()
confignew.read(cfgfile)
funcs = confignew.defaults()
c_functions = sys.modules[__name__]


def execute_function(f, *args, **kwargs):  # create a function
    f(*args, **kwargs)


allfu = []
for (
    fname,
    descri,
    function_prefix,
    functionnormalprefix,
    restype,
    argtypes,
) in allargtypes:
    fun = lib.__getattr__(funcs[fname])
    fun.restype = restype
    if len(argtypes) != 0:
        fun.argtypes = argtypes
    allfu.append((fname, fun))
    setattr(c_functions, f"{functionnormalprefix}{fname}", fun)
    setattr(
        c_functions,
        f"{function_prefix}{fname}",
        FlexiblePartialOwnName(execute_function, descri, True, fun),
    )
