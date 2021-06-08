from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="rss_reader",
    version="0.2",
    author="Anna Zaretskaya",
    author_email="econometrics@inbox.ru",
    description="A sample RSS reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AZaretskaya/PythonFinalTask",
    packages=find_packages(include=["rss_reader"]),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'rss_reader=rss_reader.rss_reader:main',
        ],
    },

)
