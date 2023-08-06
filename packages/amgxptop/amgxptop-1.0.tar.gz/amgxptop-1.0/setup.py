from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0'
DESCRIPTION = 'Request Package LMAO'

# Setting up
setup(
    name="amgxptop",
    version=VERSION,
    author="amgxp",
    author_email="<Amgxpp@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['vardxg'],
    keywords=['requests'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
