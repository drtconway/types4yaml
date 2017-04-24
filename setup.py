from setuptools import setup, find_packages

setup(
    name='type4yaml',
    version='1.0',
    packages=find_packages(),
    install_requires=['docopt', 'PyYAML'],

    author='Thomas Conway',
    author_email='drtomc@gmail.com',
    description='A basic type schema for JSON/YAML data'
)
