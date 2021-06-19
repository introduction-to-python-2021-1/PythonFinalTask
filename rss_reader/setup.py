from setuptools import setup, find_packages


with open("../requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="rss_reader",
    version="4.1",
    description="Pure Python RSS reader",
    url="https://github.com/jesuisbourrasque/PythonFinalTask",
    author="Nikita Isakov",
    author_email="jesuisbourrasque@gmail.com",
    packages=find_packages(include=["rss_reader"]),
    install_requires=required,
    entry_points={"console_scripts": ["rss-reader=rss_reader.main:main"]},
)
