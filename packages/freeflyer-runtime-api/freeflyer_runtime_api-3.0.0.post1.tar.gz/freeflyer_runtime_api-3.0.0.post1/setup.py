# coding=utf-8


import setuptools


# Use the README file as the long description
with open("README.md", "r") as fh:
    long_description = fh.read()


# Helper function to read version string
def read_version_string(filename):
    with open(filename) as fh:
        code = compile(fh.read(), filename, 'exec')
    globals_ = dict()
    locals_ = dict()
    exec(code, globals_, locals_)
    return locals_['__version__']


setuptools.setup(
    name="freeflyer_runtime_api",
    version=read_version_string("freeflyer_runtime_api/_version.py"),
    author="a.i. solutions, Inc.",
    author_email="techsupport@ai-solutions.com",
    description="Python interface to the FreeFlyer® Runtime API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ai-solutions.com/freeflyer/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"
    ],
)
