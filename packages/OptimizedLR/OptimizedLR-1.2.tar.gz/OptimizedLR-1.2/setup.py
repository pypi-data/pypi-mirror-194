from setuptools import setup, find_packages
import codecs
import os

VERSION = 'v1.2'
DESCRIPTION = 'Learning Rate Finder'
LONG_DESCRIPTION = 'A package for finding the optimum learning rate for your deep learning model'

# Setting up
setup(
    name="OptimizedLR",
    version=VERSION,
    author="Aymane Harkati",
    author_email="<aymaneharkati@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['plotly'],
    keywords=['python', 'deep learning', 'AI', 'Optimization', 'tensor flow', 'keras'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
