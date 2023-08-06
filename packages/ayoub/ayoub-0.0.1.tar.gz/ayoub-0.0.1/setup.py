from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='ayoub',
    version='0.0.1',
    description='What Is My File Size?',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ayoub-org/ayoub',
    author='DELLOUFI Ayoub',
    author_email='delloufia@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    setup_requires=['setuptools>=38.6.0'],
)
