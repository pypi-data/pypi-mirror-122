from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'Spike_intf package'

#Setting up
setup(
    name="spike_intf",
    version=VERSION,
    author="Bhavya Mehta",
    author_email="<bhavya@mettlesemi.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'riscv-isa-sim', 'spike'],
    classifiers={
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
    }
)


