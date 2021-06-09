from setuptools import setup
from reader_app.rss_reader import VERSION


setup(
    name='rss-reader',
    version=f'{VERSION}',
    author='Raman Maladziashyn',
    author_email='maladziashyn@tut.by',
    packages=['reader_app'],
    include_package_data=True,
    install_requires=['bs4==0.0.1', 'requests==2.25.1', 'validators==0.18.2'],
    entry_points={'console_scripts': ['rss_reader = reader_app.rss_reader:main', ]}
)
