#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='rclonedeobscure',
      version='1.0',
      description='A simple script to decrypt obscured/encrypted passwords from rclone',
      long_description=open('rclonedeobscure/README.md').read(),
      long_description_content_type='text/markdown; charset=UTF-8;',
      url='https://github.com/maaaaz/rclonedeobscure',
      author='Thomas D.',
      author_email='tdebize@mail.com',
      license='MIT',
      classifiers=[
        'Topic :: Security',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
      ],
      keywords='rclone deobscure obscure encrypt decrypt password',
      packages=find_packages(),
      install_requires=['pycryptodome'],
      python_requires='>=3',
      entry_points = {
        'console_scripts': ['rclonedeobscure=rclonedeobscure.rclonedeobscure:main'],
      },
      include_package_data=True)