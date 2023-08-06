from setuptools import find_packages, setup
from Cython.Build import cythonize

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="fast_bio",
    version="0.0.1",
    packages=find_packages(),
    author="Cadel Watson",
    description="Fast utilities for bioinformatics, written in Cython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    ext_modules=cythonize(["fast_bio/__init__.pyx"]),
    install_requires=[],
)
