# Copyright (c) PyBW
# Distributed under the terms of the MIT License.

from __future__ import annotations

import platform
import sys

import numpy
from setuptools import setup, find_packages

is_win_64 = sys.platform.startswith('win') and platform.machine().endswith('64')
extra_link_args = ['-Wl,--allow-multiple-definition'] if is_win_64 else []

with open('README.md') as file:
    readme = file.read()


setup(
    name='pybw',
    version='2023.2.28',
    python_requires='>=3.6',
    
    author='Bowei Pu',
    author_email='pubowei@foxmail.com',
    maintainer='Bowei Pu',
    maintainer_email='pubowei@foxmail.com',
    
    description='pybw',
    long_description=readme, 
    long_description_content_type='text/markdown',
    url='https://pubowei.cn',
    keywords=['pybw', 'tools'],
    license='MIT',
    
    packages = find_packages(), 
    
    install_requires=[
        'pathlib>=1.0.1',
        'tqdm',
    ],
    extras_require={
        'ase': ['ase>=1.0'],
    },
    project_urls={
        'Docs': 'https://pubowei.cn',
        'Package': 'https://pypi.org/project/pybw',
        'Repo': 'https://gitee.com/pubowei/pybw',
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
