#!/usr/bin/env python

from setuptools import setup, find_packages
descr = "Utility functions to parse Ardupilot's log file in bin format. \n Contains file converter from Ardupilot's log files in bin format to CSV files."

setup(
    name='pybinlog',
    description=descr,
    url='https://github.com/tayyabkhalil-313/pybinlog',
    author='Tayyab Khalil',
    author_email='tayyabkhalilpm@gmail.com',
    download_url='https://github.com/tayyabkhalil-313/pybinlog',
    license='MIT License',
    install_requires=['pymavlink'],
    packages=find_packages(),
    version="0.2.1",
    entry_points = {
        'console_scripts': [
            'bin2csv=utils.bin2csv:main',
        ],
    },
)
