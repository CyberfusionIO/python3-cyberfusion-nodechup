"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fast_redirect",
    version="1.0.5",
    description="Fast Redirect redirects domains.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    author="William Edwards",
    author_email="support@cyberfusion.nl",
    url="https://github.com/CyberfusionIO/Fast-Redirect",
    platforms=["linux"],
    packages=find_packages(
        include=[
            "fast_redirect",
            "fast_redirect.*",
        ]
    ),
    data_files=[],
    entry_points={
        "console_scripts": ["fast-redirect=fast_redirect.server:main"]
    },
    install_requires=[
        "starlette==0.31.0",
        "uvicorn==0.23.2",
        "validators==0.20.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["cyberfusion", "starlette"],
    license="MIT",
)
