#!/usr/bin/env python3
from setuptools import setup
from dogpt import get_version


with open("README.md") as f:
    readme = f.read()
with open("CHANGES.md") as f:
    changes = f.read()


setup(
    name="dogpt",
    version=get_version(),
    description="Advanced AI, but for dogs. 🐶",
    long_description_content_type="text/markdown",
    long_description=readme + "\n\n" + changes,
    author="Nicholas H.Tollervey",
    author_email="ntoll@ntoll.org",
    url="https://github.com/ntoll/dogpt",
    py_modules=["dogpt",],
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Topic :: Communications",
        "Topic :: Software Development :: Internationalization",
    ],
    entry_points={"console_scripts": ["dogpt=dogpt:command"],},
)
