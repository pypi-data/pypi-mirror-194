import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "leclerc",
    version = "0.0.1",
    author = "Luke Marhsall and Hoshang Mehta",
    author_email = "luke.marshal@suncable.energy",
    description = ("Leclerc conducts a montecarlo analysis on a range of levelised cost files"),
    license = "Open Souce",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=[],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)