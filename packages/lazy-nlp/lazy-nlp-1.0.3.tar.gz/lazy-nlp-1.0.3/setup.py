from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.3'
DESCRIPTION = 'A simple Python package that allows you to do zeroshot, embeddings and build a classifier. See here for more information: https://github.com/LeonardPuettmann/lazy-nlp'

# Setting up
setup(
    name="lazy-nlp",
    version=VERSION,
    author="Leonard Püttmann",
    author_email="<leopuettmann@outlook.de>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["transformers", "torch", "sentence-transformers", "scikit-learn", "numpy"],
    keywords=["python", "zeroshot", "nlp", "lazy-nlp"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)