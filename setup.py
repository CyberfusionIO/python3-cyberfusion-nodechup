"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nodechup",
    version="1.0",
    description="Program to manage Node.js installations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    author="William Edwards",
    author_email="opensource@cyberfusion.nl",
    url="https://github.com/CyberfusionNL/NodeCHUP",
    platforms=["linux"],
    packages=find_packages(
        include=[
            "nodechup",
            "nodechup.*",
        ]
    ),
    data_files=[],
    install_requires=["requests==2.27.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["cyberfusion", "nodejs"],
    license="MIT",
)
