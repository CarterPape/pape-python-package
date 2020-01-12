# This program is free software. See file LICENSE for details.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pape",
    version="0.0.1",
    author="Carter Pape",
    author_email="pape-python-package@carterpape.com",
    description="A package for personalized Python add-ons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CarterPape/pape-python-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires='>=3',
)
