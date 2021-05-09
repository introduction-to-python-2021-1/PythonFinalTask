from setuptools import setup

setup(
    name='rss-reader',
    version='0.2',
    description='Command-line RSS reader',
    author='Sergey Rutkovskiy',
    url='https://github.com/spectraise/PythonFinalTask',
    packages=['rss_reader', 'components', ],
    install_requires=['bs4==0.0.1', 'beautifulsoup4==4.9.3', 'lxml==4.6.3', 'python-dateutil==2.8.1',
                      'requests==2.25.1', ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'rss_reader = rss_reader.rss_reader:main',
        ]
    }
)
