from setuptools import setup
from os.path import join, dirname

setup(
    name='rss_reader',
    version='1.0',
    packages=['rss_reader'],
    author='Natallia Patsiomkina',
    author_email='patsiomkina@inbox.ru',
    description='Pure Python command-line RSS reader',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=['dateparser', 'feedparser'],
    entry_points={
        'console_scripts': 'rss_reader = rss_reader.rss_reader:main'
    }
)
