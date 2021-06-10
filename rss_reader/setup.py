from os.path import dirname, join

from setuptools import setup, find_packages

with open(join(dirname(dirname(__file__)), 'requirements.txt'), 'r') as file:
    requirements = file.read().splitlines()

setup(
    name='rss_reader',
    version=2.1,
    description='Pure Python command-line RSS reader',
    author='Eduard Vasanski',
    author_email='wasanski@mail.ru',
    url='https://github.com/EVasanski/PythonFinalTask',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rss_reader = rss_reader.rss_reader:main',
        ]
    },
    install_requires=requirements,
)
