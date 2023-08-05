from setuptools import setup, find_packages
import os

VERSION = '1.0.0'
DESCRIPTION = 'basic useful tools'
LONG_DESCRIPTION = 'A package that has some useful tools.'

# Setting up
setup(
    name="jakubsulla",
    version=VERSION,
    author="Jakubsulla (Jakub Šulla)",
    author_email="<support@jakubsulla.tk>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tools', 'simple', 'hello', 'testing'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)