from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

# define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

ext = Extension(
    name="run_cythonized",
    sources=["run_cythonized.pyx"],
    include_dirs=[numpy.get_include()],
    extra_compile_args=["-ffast-math"])
setup(ext_modules=cythonize(ext))


# http://nealhughes.net/cython1/
