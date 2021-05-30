from setuptools import setup
from pathlib import Path

VERSION = 2.0
AUTHOR = "Evzhenko Ilya"
EMAIL = "evzhenko1106@gmail.com"
DESCRIPTION = "Pure Python command-line RSS reader."

BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_DIR = BASE_DIR / "rss_reader"
README = BASE_DIR / "README.md"

with open(README, "r") as fp:
    readme = fp.read()


setup(
    name="rss_reader",
    version=f"{VERSION}",
    author=f"{AUTHOR}",
    author_email=f"{EMAIL}",
    description=(f"{DESCRIPTION}"),
    license="BSD",
    packages=["rss_reader"],
    long_description=readme,
    entry_points={
        "console_scripts": [
            "rss_reader=rss_reader.rss_reader:main",
        ],
    },
)
