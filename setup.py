import setuptools
# from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="rss_reader",
    version="0.2",
    author="Anna Zaretskaya",
    author_email="econometrics@inbox.ru",
    description="A sample RSS reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AZaretskaya/PythonFinalTask",
    package_dir={"": "rss_reader"},
    # packages=setuptools.find_packages(where="rss_reader"),
    python_requires=">=3.8",
    # install_requires=[
    #     "argparse"
    #     "requests",
    #     "bs4"
    #     "BeautifulSoup",
    #     "json",
    #     "libcairo-2"
    # ],
    entry_points={
        'console_scripts': [
            'rss_reader=rss_reader.rss_reader:main',
        ],
    },

)
