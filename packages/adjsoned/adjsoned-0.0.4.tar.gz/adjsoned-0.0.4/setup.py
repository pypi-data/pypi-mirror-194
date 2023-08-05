import os

from codecs import open
from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="adjsoned",
    version="0.0.4",
    description="Loads required properties/config from a json file to a Python runtime object",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://adjsoned.readthedocs.io/",
    author="Dan Demidov",
    author_email="demidob.dev@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    packages=["adjsoned"],
    include_package_data=True
)
