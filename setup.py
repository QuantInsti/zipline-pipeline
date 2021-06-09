# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 17:09:36 2018

@author: prodipta
"""
import os
import numpy as np
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext as _build_ext
__package_name__ = "zipline_pipeline"
setup_path = os.path.abspath(os.path.dirname(__file__))
versioneer = "version.py"
# lazy loading of cython, see below:
# https://stackoverflow.com/questions/37471313/setup-requires-with-cython
try:
    from Cython.Build import cythonize
except ImportError:
     def cythonize(*args, **kwargs):
         from Cython.Build import cythonize
         return cythonize(*args, **kwargs)

# read versioning
namespace = {}
with open(os.path.join(setup_path, __package_name__, versioneer)) as fp:
    code = compile(fp.read(), versioneer, 'exec')
    exec(code, namespace)

# read requirements.txt for dependencies
def parse_requirements(requirements_txt):
    with open(requirements_txt) as f:
        for line in f.read().splitlines():
            if not line or line.startswith("#"):
                continue
            yield line

def install_requires():
    return list(set([r for r in parse_requirements('requirements.txt')]))


ext_modules = [
        Extension('zipline_pipeline.lib._factorize', ['zipline_pipeline/lib/_factorize.pyx']),
        Extension('zipline_pipeline.lib._float64window', ['zipline_pipeline/lib/_float64window.pyx']),
        Extension('zipline_pipeline.lib._int64window', ['zipline_pipeline/lib/_int64window.pyx']),
        Extension('zipline_pipeline.lib._labelwindow', ['zipline_pipeline/lib/_labelwindow.pyx']),
        Extension('zipline_pipeline.lib._uint8window', ['zipline_pipeline/lib/_uint8window.pyx']),
        Extension('zipline_pipeline.lib.adjustment', ['zipline_pipeline/lib/adjustment.pyx']),
        Extension('zipline_pipeline.lib.rank', ['zipline_pipeline/lib/rank.pyx']),
        Extension('zipline_pipeline.data._adjustments', ['zipline_pipeline/data/_adjustments.pyx']),
        ]

for ext in ext_modules:
    # The Numpy C headers are currently required
    ext.include_dirs.append(np.get_include())

setup(
    name=__package_name__,
    url=namespace["__url__"],
    version= namespace["__version__"],
    description=namespace["__description__"],
    long_description=namespace["__long_desc__"],
    author=namespace["__author__"],
    author_email=namespace["__email__"],
    packages=find_packages(include=['zipline_pipeline', 'zipline_pipeline.*']),
    ext_modules=cythonize(ext_modules),
    include_dirs=[np.get_include()],
    include_package_data=False,
    license=namespace["__license__"],
    classifiers=namespace["__package_classifier__"],
    install_requires=install_requires()
)
