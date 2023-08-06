from setuptools import setup

setup(
    name='my_dummy_package',
    version='0.1.1',
    description='My own dummy package for lab2',
    url='',
    install_requires=['pandas<1.2.4'],
    packages=['mypackage'],
)