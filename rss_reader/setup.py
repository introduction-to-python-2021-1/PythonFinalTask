"""
Allow users use the reader without python installation, just with bash.
"""

from setuptools import setup, find_packages

setup(
    name="rss_reader",
    version="4.0.2",
    description="Python RSS-reader with possibility to open from bash without installation",
    url="https://github.com/Bulachka/PythonFinalTask",
    author="Valodzina Aliaksandra",
    keywords="rss_reader",
    packages=find_packages(include=["rss_reader", "rss_reader.*", "main_reader", "main_reader.*"]),
    package_data={
        "rss_reader": ["package_data/**/*"]
    },
    install_requires=["feedparser==6.0.2", "dateparser==1.0.0", "xhtml2pdf==0.2.5", "Jinja2==3.0.1"],
    entry_points={
        "console_scripts": [
            "rss_reader=main_reader.rss_reader:main",
        ],
    },
)
