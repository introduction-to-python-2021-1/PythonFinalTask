from setuptools import setup, find_packages
from os.path import join, dirname

with open(file=join(dirname(dirname(__file__)), 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name='rss_reader',
    version=1.1,
    description='Pure Python command-line RSS reader',
    author='Eduard Vasanski',
    author_email='wasanski@mail.ru',
    url='https://github.com/EVasanski/PythonFinalTask',
    packages=find_packages(['rss_reader', 'tests']),
    entry_points={
        'console_scripts': [
            'rss_reader = rss_reader.rss_reader:main',
        ]
    },
    install_requires=required,
)
