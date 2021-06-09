from pathlib import Path

from setuptools import setup

VERSION = 4.0
AUTHOR = "Evzhenko Ilya"
EMAIL = "evzhenko1106@gmail.com"
DESCRIPTION = "Pure Python command-line RSS reader."

BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_DIR = BASE_DIR / "rss_reader"


setup(
    name="rss_reader",
    version=f"{VERSION}",
    author=f"{AUTHOR}",
    author_email=f"{EMAIL}",
    description=(f"{DESCRIPTION}"),
    license="BSD",
    packages=["rss_reader"],
    entry_points={
        "console_scripts": [
            "rss_reader=rss_reader.rss_reader:main",
        ],
    },
)
