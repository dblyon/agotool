from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy


ext = Extension(
    name="run_cythonized",
    sources=["run_cythonized.pyx"],
    include_dirs=[numpy.get_include()],
    extra_compile_args=["-ffast-math"])
setup(ext_modules=cythonize(ext))


# http://nealhughes.net/cython1/


### setup_map.py
# from distutils.core import setup
# from distutils.extension import Extension
# from Cython.Build import cythonize
# from Cython.Distutils import build_ext
#
# import os
#
# os.environ["CC"] = "g++"
# os.environ["CXX"] = "g++"
#
#
# modules = [Extension("map_example",
#                  ["map_example.pyx"],
#                  language = "c++",
#                  extra_compile_args=["-std=c++11"],
#                  extra_link_args=["-std=c++11"])]
#
# setup(name="map_example",
#      cmdclass={"build_ext": build_ext},
#      ext_modules=modules)

# g++ -DNDEBUG -fwrapv -O2 -Wall -Wstrict-prototypes -march=core2 -mssse3 -ftree-vectorize -fPIC -fPIE -O2 -pipe -D_FORTIFY_SOURCE=2 -mmacosx-version-min=10.9 -I/Users/dblyon/anaconda3/envs/agotool/include/python3.6m -c map_example.cpp -o build/temp.macosx-10.9-x86_64-3.6/map_example.o -std=c++11
