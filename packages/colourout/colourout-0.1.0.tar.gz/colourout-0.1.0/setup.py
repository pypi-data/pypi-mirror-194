"""Setup script for the colourout package."""
from __future__ import annotations

import setuptools

import colourout

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colourout",
    version=colourout.__version__,
    description="A Python package for printing coloured text to the terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sam-kenney/colourout",
    author="Sam Kenney",
    author_email="sam.kenney@me.com",
    license="MIT",
    packages=["colourout"]
    + [f"colourout.{sub}" for sub in setuptools.find_packages("colourout")],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
