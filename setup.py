#! /usr/bin/env python
import os
from setuptools import setup

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
with open(README_PATH, "r") as f:
    README = f.read()

setup(
    name="ariadne",
    author="Mirumee Software",
    author_email="hello@mirumee.com",
    description="Ariadne is a Python library for implementing GraphQL servers.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="BSD",
    version="100.1.0",
    url="https://github.com/mirumee/ariadne",
    packages=["ariadne"],
    include_package_data=True,
    install_requires=[
        "graphql-core@https://github.com/nudjur/graphql-core/archive/master.zip#egg=graphql-core-2.0.0",
        "python-multipart>=0.0.5",
        "starlette<0.13",
        "typing_extensions>=3.6.0",
    ],
    classifiers=CLASSIFIERS,
    platforms=["any"],
    zip_safe=False,
)
