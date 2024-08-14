"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nodechup",
    version="1.2.1.2",
    description="Use nodechup to install multiple Node.js versions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cyberfusion",
    author_email="support@cyberfusion.io",
    url="https://github.com/CyberfusionIO/nodechup",
    platforms=["linux"],
    packages=find_packages(
        include=[
            "nodechup",
            "nodechup.*",
        ]
    ),
    data_files=[],
    entry_points={"console_scripts": ["nodechup=nodechup.CLI:main"]},
    install_requires=["docopt==0.6.2", "schema==0.7.7", "requests==2.32.3"],
)
