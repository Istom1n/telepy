#!/usr/bin/env python

import os
from setuptools import setup

setup(name='telepy',
      version='0.0.1',
      description='Telepy is incredible, ultra-fast wrapper for TDLib, a cross-platform, fully functional Telegram client.',
      url='https://github.com/Ivan-Istomin/telepy/',
      maintainer='Ivan Istomin',
      maintainer_email='istom1n@pm.me',
      license='MIT',
      keywords='wrapper,telegram,messaging,api',
      packages=['telepy'],
      install_requires=open('requirements.txt').read().strip().split('\n'),
      long_description=(open('README.md').read() if os.path.exists('README.md')
                        else ''),
    #   setup_requires=['pytest-runner'],
    #   tests_require=['pytest'],
      zip_safe=False)