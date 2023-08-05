from setuptools import setup

setup(
    name = "maxez",
    version = "0.0.2",
    description = "Math Package",
    py_modules = ["hello"],
    package_dir = {'': 'maxez'},
)

#python setup.py sdist bdist_wheel