from setuptools import setup

setup(
    name='rss-reader',
    version='0.1',
    description='Command-line RSS reader',
    author='Kolesnikov Viktor',
    url='https://github.com/MackDillan/EPAMFinalTask',
    install_requires=['beautifulsoup4==4.9.3', 'lxml==4.6.3'],
    python_requires='>=3.8',
    packages=['utils'],
    scripts=['rss_reader.py'],
)
