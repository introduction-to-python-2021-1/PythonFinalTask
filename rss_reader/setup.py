from setuptools import setup

setup(
    name='rss_reader',
    version='1.2',
    packages=['rss_reader'],
    author='Natallia Patsiomkina',
    author_email='patsiomkina@inbox.ru',
    description='Pure Python command-line RSS reader',
    install_requires=['dateparser', 'feedparser'],
    entry_points={
        'console_scripts': 'rss_reader = rss_reader.rss_reader:main'
    }
)
