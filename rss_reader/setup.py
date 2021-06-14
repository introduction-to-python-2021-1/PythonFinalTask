import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rss_reader",
    version="1.4",
    author="Margarita Bobich",
    author_email="bobich.margarita@gmail.com",
    description="RSS reader is a command-line utility which receives RSS URL and prints results in readable format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/margarita-bobich/PythonFinalTask/tree/main/rss_reader",
    packages=setuptools.find_packages(exclude=("tests",)),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'rss_reader = rssreader.rss_reader:main',
        ],
    },
    install_requires=[
        'elementpath', 'requests', 'argparse', 'jinja2', 'xhtml2pdf', 'ddt',
    ],
    zip_safe=False
)
