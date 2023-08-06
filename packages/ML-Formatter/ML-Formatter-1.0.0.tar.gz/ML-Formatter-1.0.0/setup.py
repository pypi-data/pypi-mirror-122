import re

import setuptools


with open("readme.md", "r") as fh:
    long_description = fh.read()

_version_regex = (
    r"^__version__ = ('|\")((?:[0-9]+\.)*[0-9]+(?:\.?([a-z]+)(?:\.?[0-9])?)?)\1$"
)

with open("formatter/__init__.py") as stream:
    match = re.search(_version_regex, stream.read(), re.MULTILINE)

version = match.group(2)

setuptools.setup(
    name="ML-Formatter",
    version=version,
    author="Skelmis",
    author_email="ethan@koldfusion.xyz",
    description="An easy to use package for parsing media and transforming it for your Machine Learning projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Skelmis/ML-Formatter",
    packages=setuptools.find_packages(),
    install_requires=["attrs"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires=">=3.6",
)
