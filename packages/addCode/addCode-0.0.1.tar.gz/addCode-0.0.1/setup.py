from setuptools import setup

setup(
    name = 'addCode',
    version = '0.0.1',
    description = 'Add two numbers!',
    long_description = "Very basic function for adding two numbers.",
    py_modules = ["addCode"],
    package_dir = {'': 'src'},
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    intall_requires = [
        ],
)
