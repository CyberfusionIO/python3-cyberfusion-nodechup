"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fast_redirect",
    version="1.0.5",
    description="fast-redirect redirects domains.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cyberfusion",
    author_email="support@cyberfusion.io",
    url="https://github.com/CyberfusionIO/fast-redirect",
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
        "starlette==0.38.2",
        "uvicorn==0.30.6",
        "validators==0.33.0",
    ],
)
