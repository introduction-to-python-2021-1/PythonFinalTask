from setuptools import setup

from rss_reader.rss_reader import VERSION

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="rss_reader",
    version=VERSION,
    description="Pure Python command-line RSS reader.",
    long_description=readme,
    url="https://github.com/egor-makhlaev/PythonFinalTask/tree/final-task-implementation",
    author="Egor Makhlaev",
    author_email="egor.makhlaev@gmail.com",
    license=license,
    packages=["rss_reader"],
    install_requires=["dateparser"],
    entry_points={
        'console_scripts': [
            'rss_reader=rss_reader.rss_reader:main',
        ],
    }
)
