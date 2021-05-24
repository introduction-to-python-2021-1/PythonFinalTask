from setuptools import setup

setup(
    name='reader',
    version='1.3',
    packages=['reader'],
    author='Natallia Patsiomkina',
    author_email='patsiomkina@inbox.ru',
    description='Pure Python command-line RSS reader',
    install_requires=['dateparser', 'feedparser'],
    entry_points={
        'console_scripts': 'reader = reader.rss_reader:main'
    }
)
