import setuptools
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="PythonFinalTask_Anna_Zaretskaya",
    version="0.3",
    author="Anna Zaretskaya",
    author_email="econometrics@inbox.ru",
    description="A sample RSS reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "rss_reader"},
    packages=setuptools.find_packages(where="rss_reader"),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'rss_reader=rss_reader:main',
        ],
    },

)
