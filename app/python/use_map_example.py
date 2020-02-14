import map_example

C_MAXV = 100000000
C_NUMBER = 10

def cython_cpp_book_notation():
    x = 1
    while(x<C_MAXV):
        map_example.example_cpp_book_notation(x)
        x *= 10

def cython_cpp_python_notation():
    x = 1
    while(x<C_MAXV):
        map_example.example_cpp_python_notation(x)
        x *= 10

def cython_ctyped_notation():
    x = 1
    while(x<C_MAXV):
        map_example.example_ctyped_notation(x)
        x *= 10


def pure_python():
    x = 1
    while(x<C_MAXV):
        map_a = {}
        for i in range(x):
            map_a[i] = i
        x *= 10
    return 0


if __name__ == '__main__':
    import timeit

    print("Cython CPP book notation")
    print(timeit.timeit("cython_cpp_book_notation()", setup="from __main__ import cython_cpp_book_notation", number=C_NUMBER))


    print("Cython CPP python notation")
    print(timeit.timeit("cython_cpp_python_notation()", setup="from __main__ import cython_cpp_python_notation", number=C_NUMBER))


    print("Cython python notation")
    print(timeit.timeit("cython_ctyped_notation()", setup="from __main__ import cython_ctyped_notation", number=C_NUMBER))

    print("Pure python")
    print(timeit.timeit("pure_python()", setup="from __main__ import pure_python", number=C_NUMBER))
