from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pypiage",
    version="0.1.0",
    author="chrisjsimpson",
    author_email="oss@karmacomputing.co.uk",
    description="A package for finding the least updated packages your project depends on.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisjsimpson/pypiage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
