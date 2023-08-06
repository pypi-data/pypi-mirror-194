#!/usr/bin/env python3

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="iocbio.kinetics",
    version="1.5.0",
    description="IOCBio Kinetics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="IOCBio team",
    author_email="iocbio@sysbio.ioc.ee",
    license="GPLv3",
    url="https://sysbio.ioc.ee",
    packages=[
        "iocbio.kinetics",
        "iocbio.kinetics.app",
        "iocbio.kinetics.calc",
        "iocbio.kinetics.gui",
        "iocbio.kinetics.handler",
        "iocbio.kinetics.io"
    ],
    entry_points={
        "gui_scripts": [
            "iocbio-kinetics=iocbio.kinetics.app.gui:main",
            "iocbio-banova=iocbio.kinetics.app.banova:main",
            "iocbio-fetch=iocbio.kinetics.app.fetch:main",
            "iocbio-fetch-repeated=iocbio.kinetics.app.fetch_repeated:main",
        ],
    },
    include_package_data=True,
    package_data={"iocbio.kinetics.app": ["*.png"]},
    install_requires=[
        "iocbio.db >= 2.0",
        "PySide6",
        "h5py",
        "scipy",
        "numpy",
        "pyqtgraph",
        "XlsxWriter",
        "tabulate",
        "msgpack",
        "attrdict3",
        "netCDF4",
        "python-dateutil",
        "tifffile",
    ],
    keywords=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
