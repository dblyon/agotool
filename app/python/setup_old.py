from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy


ext = Extension(name="run_cythonized_old", sources=["run_cythonized_old.pyx"],
    include_dirs=[numpy.get_include()])
setup(ext_modules=cythonize(ext))
