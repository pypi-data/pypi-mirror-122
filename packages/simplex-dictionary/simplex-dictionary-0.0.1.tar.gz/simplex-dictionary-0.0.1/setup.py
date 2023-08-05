# -*- encoding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

test_requires = ["pytest", "mypy", "black", "flake8", "flake8-black"]

setuptools.setup(
    name="simplex-dictionary",
    version="0.0.1",
    author="Mikaël Capelle",
    author_email="capelle.mikael@gmail.com",
    description="Implementation of a simplex dictionary in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitea.typename.fr/mikael.capelle/simplex",
    packages=setuptools.find_packages(),
    install_requires=[],
    test_requires=test_requires,
    extras_require={"test": test_requires},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
