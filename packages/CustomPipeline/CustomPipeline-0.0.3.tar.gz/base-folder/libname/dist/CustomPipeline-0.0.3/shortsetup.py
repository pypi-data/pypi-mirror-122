from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'Panda3d Render PipeLine Test'
LONG_DESCRIPTION = 'Panda3d Render Pipe use for testing.'

# Setting up
setup(
    name="CustomPipeline",
    version=VERSION,
    author="Micheal (Micheal Jackson)",
    author_email="<none@mymail.cock>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['panda3d', 'render', 'custom pipeline', 'hidden', 'self use'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)