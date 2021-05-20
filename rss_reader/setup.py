from setuptools import setup

setup(
    name='rss_reader',
    version='0.1',
    description='Command-line RSS reader',
    author='Kolesnikov Viktor',
    url='https://github.com/MackDillan/PythonFinalTask',
    install_requires=['beautifulsoup4', 'lxml', 'requests'],
    python_requires='>=3.8',
    packages=['rss_reader'],
    entry_points={
        'console_scripts': [
            'rss_reader=rss_reader.rss_reader:main',
        ],
    }
)
