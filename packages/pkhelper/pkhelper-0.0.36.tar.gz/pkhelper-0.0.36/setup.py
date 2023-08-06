#!/usr/bin/python3
from setuptools import setup, find_packages
__version__="0.0.36"

def get_long_description():
    with open("README.md") as f:
        long_description = f.read()
    try:
        import github2pypi
        return github2pypi.replace_url(slug="pk-628996/pkhelper", content=long_description)
    except Exception:
        return long_description

setup(
    name="pkhelper",
    version=f"{__version__}",
    packages=['pkhelper'],
    py_modules=['pkhelper'],
    description="A module for some common things",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    download_url=f'https://github.com/pk-628996/pkhelper/archive/refs/tags/v{__version__}-alpha.zip',
    url='https://github.com/pk-628996/pkhelper',
    license="MIT",
    install_requires=['requests','gdown','aiohttp','cloudscraper','beautifulsoup4', 'youtube_transcript_api' ],
    entry_points={"console_scripts": ["pkhelper=pkhelper.cli:main"]},
)
