# cython: language_level=3, nonecheck=True, boundscheck=False, wraparound=False, profile=False

import Cython

from libcpp.unordered_map cimport unordered_map
from libcpp.pair cimport pair

cpdef int example_cpp_book_notation(int limit):
    cdef unordered_map[int, int] mapa
    cdef pair[int, int] entry

    cdef int i

    for i in range(limit):
        entry.first = i
        entry.second = i
        mapa.insert(entry)
    return 0

cpdef int example_cpp_python_notation(int limit):
    cdef unordered_map[int, int] mapa
    cdef pair[int, int] entry

    cdef int i

    for i in range(limit):
        mapa[i] = i

    return 0


cpdef int example_ctyped_notation(int limit):
    mapa = {}
    cdef int i
    for i in range(limit):
        mapa[i] = i
    return 0
