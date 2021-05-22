from setuptools import setup, find_packages

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
    }
)
