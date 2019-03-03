import os
from setuptools import setup

def load_file(name):
    with open(name, 'r') as f:
        return f.read()

setup(
    name="web-smoke",
    version="0.1.0",
    author="Alexei Kornienko",
    author_email="alexei.kornienko@gmail.com",
    url="https://github.com/Alexei-Kornienko/web-smoke",
    description="Minimal smoketest framework",
    long_description=load_file('README.md'),
    install_requires=load_file('requirements.txt'),
    scripts=[],
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
