from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy


ext = Extension(name="run_cythonized_20181112", sources=["run_cythonized_20181112.pyx"],
    include_dirs=[numpy.get_include()])
setup(ext_modules=cythonize(ext))
