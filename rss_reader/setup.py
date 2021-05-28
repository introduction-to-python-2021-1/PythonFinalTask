from setuptools import setup

setup(
    name='rss_reader',
    version='0.2',
    description='Command-line RSS reader',
    author='Kolesnikov Viktor',
    url='https://github.com/MackDillan/PythonFinalTask',
    install_requires=['beautifulsoup4', 'lxml', 'requests', 'python-dateutil', ],
    python_requires='>=3.8',
    packages=['rss_reader'],
    package_data={
            'components': ['tests/rss_feed.xml']
        },
    entry_points={
        'console_scripts': [
            'rss_reader=rss_reader.rss_reader:main',
        ],
    }
)
