# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 17:09:36 2018

@author: prodipta
"""
import os
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext as _build_ext

# https://stackoverflow.com/questions/37471313/setup-requires-with-cython
try:
    from Cython.Build import cythonize
except ImportError:
     def cythonize(*args, **kwargs):
         from Cython.Build import cythonize
         return cythonize(*args, **kwargs)

__package_name__ = "zipline_pipeline"
setup_path = os.path.abspath(os.path.dirname(__file__))
versioneer = "version.py"

namespace = {}
with open(os.path.join(setup_path, __package_name__, versioneer)) as fp:
    code = compile(fp.read(), versioneer, 'exec')
    exec(code, namespace)

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

ext_modules = cythonize(ext_modules, compiler_directives={'language_level' : "3"})
    
class custom_build_ext(_build_ext):
    """
        build_ext command for use when numpy headers are needed.
        see https://stackoverflow.com/questions/2379898/make\
        -distutils-look-for-numpy-header-files-in-the-correct-place
    """
    def run(self):
        import numpy
        self.include_dirs.append(numpy.get_include())
        return super().run()
        
    def initialize_options(self):
        super().initialize_options()
        if self.distribution.ext_modules == None:
            self.distribution.ext_modules = []

        self.distribution.ext_modules.extend(ext_modules)

setup(
    name=__package_name__,
    cmdclass = {'build_ext': custom_build_ext},
    url=namespace["__url__"],
    version= namespace["__version__"],
    description=namespace["__description__"],
    long_description=namespace["__long_desc__"],
    author=namespace["__author__"],
    author_email=namespace["__email__"],
    packages=find_packages(
            include=['zipline_pipeline', 'zipline_pipeline.*']),
    ext_modules=cythonize(ext_modules),
    include_package_data=False,
    license=namespace["__license__"],
    classifiers=namespace["__package_classifier__"],
)
