from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.4'
DESCRIPTION = 'A python module for bitclout'
LONG_DESCRIPTION = 'A package that allows to fetch various information from the bitclout blockchain using the bitclout APIs. BitClout is a decentralised social media network'

# Setting up
setup(
    name="bitclout",
    version= VERSION,
    author="ItsAditya (https://bitclout.com/u/ItsAditya)",
    author_email="<chaudharyaditya0005@gmail.com>",
    description="A python module for bitclout",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'bitclout', 'social media', 'crypto', 'blockchain', 'decentralisation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)