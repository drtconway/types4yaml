from setuptools import setup, find_packages

setup(
    name='types4yaml',
    version='1.0',
    packages=find_packages(),
    install_requires=['docopt', 'PyYAML'],

    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    author='Thomas Conway',
    author_email='drtomc@gmail.com',
    description='A basic type schema for JSON/YAML data'
)
