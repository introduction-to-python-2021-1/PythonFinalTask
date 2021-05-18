from setuptools import setup, find_packages

setup(
    name="rss_reader",
    version="1.0",
    description="Pure Python command-line RSS reader.",
    url="https://github.com/YuliyaLit/PythonFinalTask",
    author="Stralchuk Yuliya",
    author_email='Yuliya-litvinko@mail.ru',
    keywords="rss_reader",
    packages=["rss_reader"],
    install_requires=['feedparser'],
    entry_points={
        "console_scripts": [
            "rss_reader=rss_reader.rss_reader:main",
        ],
    },
)