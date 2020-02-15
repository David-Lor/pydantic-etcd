#!/usr/bin/env python

from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f.readlines() if line]

with open("requirements.test.txt") as f:
    requirements_test = [line.strip() for line in f.readlines() if line]

setup(
    name="pydantic-etcd",
    version="0.0.1",
    description="Class-based settings loader with ETCD support, working from pydantic's BaseSettings class",
    author="David Lorenzo",
    url="https://github.com/David-Lor/pydantic-etcd",
    packages=["pydantic_etcd"],
    install_requires=requirements,
    setup_requires=["pytest-runner"],
    tests_require=requirements_test,
    test_suite="pytest",
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    long_description_content_type="text/markdown",
    long_description=long_description,
)
