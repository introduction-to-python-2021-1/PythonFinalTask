import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rss_reader",
    version="1.3",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(exclude=("tests",)),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'rss_reader = rssreader.rss_reader:main',
        ],
    },
    install_requires=[
        'elementpath', 'requests', 'argparse',
    ],
    zip_safe=False
)
