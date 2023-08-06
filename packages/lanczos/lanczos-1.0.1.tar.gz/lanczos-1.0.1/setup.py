import os
import sys

from setuptools import setup, find_packages, Extension
from setuptools.command.build_py import build_py as _build_py

from numpy.distutils.misc_util import get_numpy_include_dirs
numpy_inc = get_numpy_include_dirs()

class build_py(_build_py):
    def run(self):
        self.run_command("build_ext")
        return super().run()


setup(name='lanczos',
      version='1.0.1',
      author = 'David Nidever, Dustin Lang',
      author_email = 'davidnidever@gmail.com',
      url = 'https://github.com/dnidever/lanczos',
      cmdclass={'build_py': build_py},
      packages = ["lanczos"],
      ext_modules=[
        Extension(
            'lanczos._lanczos',
            ['lanczos/lanczos3.i'],
            include_dirs=["lanczos"]+numpy_inc,
        )
    ],
)
