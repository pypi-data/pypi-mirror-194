#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:42:11 2019

@author: stefan
"""

import setuptools
from distutils.core import setup
import indago

print(f'Detected Indago version: {indago.__version__}')

with open('readme.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
    
with open('docs/source/index.rst', 'r', encoding='utf-8') as fh:
    rst_lines = fh.readlines()
rst_lines[5] = f'Welcome to Indago {indago.__version__} documentation!\n'
rst_lines[6] = '=' * (len(rst_lines[5]) - 1) + '\n'

with open('docs/source/index.rst', 'w', encoding='utf-8') as fh:
    fh.write(''.join(rst_lines))

setup(name='Indago',
      version=indago.__version__,
      description='Numerical optimization framework',
      author='sim.riteh.hr',
      author_email='stefan.ivic@riteh.hr',
      url='http://sim.riteh.hr/',
      py_modules=['indago',
                  #'indago.optimizer',
                  #'indago.pso',
                  #'indago.fwa',
                  #'indago.abca',
                  #'indago.ssa',
                  #'indago.direct_search',
                  #'indago.de',
                  #'indago.mmo',
                  'indago.benchmarks'],
      include_package_data=True,
      setup_requires=['wheel'],
      install_requires=['numpy>=1.16',
                        'matplotlib>=2',
                        'scipy',
                        'rich'
                        ],
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          ],
      python_requires='>=3.6',
)
