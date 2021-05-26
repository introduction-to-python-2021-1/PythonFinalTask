import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="rss-reader",
    version="3.0",
    author="Julia Los",
    author_email="los.julia.v@gmail.com",
    description="A Python command-line RSS reader",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    packages=['rss_reader'],
    install_requires=['feedparser>=6.0.2'],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'rss_reader = rss_reader.rss_reader:main',
        ],
    }
)
