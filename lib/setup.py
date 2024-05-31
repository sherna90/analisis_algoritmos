from setuptools import setup, Extension
from Cython.Build import cythonize


prio_q = Extension(name="priority_queue",
                   sources=["priority_queue.pyx"],
                   language="c++11", extra_compile_args=["-std=c++11 --compile-args=-fopenmp"],
                   )

setup(name="priority_queue", version="1.0.0", ext_modules=cythonize([prio_q]))
