from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Capsphere proprietary libraries'
PACKAGE_NAME = 'capsphere'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Andy Lee",
    author_email="andy.mt.lee@gmail.com",
    description=DESCRIPTION,
    keywords=['python', 'capsphere', 'pdf'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)