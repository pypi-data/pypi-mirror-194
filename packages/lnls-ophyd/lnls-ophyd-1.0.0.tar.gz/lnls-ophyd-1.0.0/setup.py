#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name="lnls-ophyd",
    version="1.0.0",
    description="LNLS OPHYD hardware abstraction",
    long_description=readme(),
    author="Hugo Campos",
    author_email="hugo.campos@lnls.br",
    url="https://gitlab.cnpem.br/SOL/bluesky/lnls-ophyd",
    install_requires=[
        "ophyd",
    ],
    package_data={},
    include_package_data=True,
    packages=find_packages(where=".", exclude=["test", "test.*", "tests"]),
)
