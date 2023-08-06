from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A library for statistical calculations.'

setup(
    name="sttc",
    version=VERSION,
    author="Dayon Oliveira",
    author_email="dayon.dos@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dayonoliveira/Statistic',
    keywords=['python', 'calc', 'statistics', 'statistic', 'sttc', 'stac', 'statistical library', 'continuous', 'discrete', 'math'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)