from setuptools import setup

setup(
    name='rss_reader',
    version='1.3',
    packages=['rss_reader'],
    install_requires=[
        'feedparser',
    ],
    entry_points={
        'console_scripts': [
            'rss_reader=rss_reader:main',
            'rss-reader=rss_reader:main',
        ],
    }
)
