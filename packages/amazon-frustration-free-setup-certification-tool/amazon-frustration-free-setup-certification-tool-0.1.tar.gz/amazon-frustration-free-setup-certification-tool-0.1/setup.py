import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='amazon-frustration-free-setup-certification-tool',
    packages=find_packages(),
    version='0.1',
    description='Automation test scripts for Amazon Frustration Free Setup certification',
    long_description=read('README.rst'),
    author='tozha',
    author_email='tozha@amazon.com',
    url='https://github.com/amzn/amazon-frustration-free-setup-certification-tool',
    keywords='amazon-frustration-free-setup-certification-tool automation_test appium pytest',
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
)
