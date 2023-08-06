#!/usr/bin/env python3

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="iocbio.db",
    version="2.0.0",
    description="IOCBio Db",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="IOCBio team",
    author_email="iocbio@sysbio.ioc.ee",
    license="GPLv3",
    url="https://sysbio.ioc.ee",
    packages=["iocbio.db"],
    entry_points={},
    setup_requires=["wheel"],
    install_requires=["PySide6", "keyring", "psycopg2-binary", "SQLAlchemy"],
    keywords=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
