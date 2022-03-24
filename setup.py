"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nodechup",
    version="1.1",
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
    entry_points={"console_scripts": ["nodechup=nodechup.CLI:main"]},
    install_requires=["docopt==0.6.2", "schema==0.7.2", "requests==2.27.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["cyberfusion", "nodejs"],
    license="MIT",
)
