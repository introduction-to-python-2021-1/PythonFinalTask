from setuptools import setup

setup(
    name='rss-reader',
    version='0.5',
    description='Command-line RSS reader',
    author='Sergey Rutkovskiy',
    url='https://github.com/spectraise/PythonFinalTask',
    packages=['rss_reader', 'components', ],
    package_data={
        'components': ['fonts/DejaVuSans.ttf', 'templates/template.html']
    },
    install_requires=['bs4==0.0.1', 'beautifulsoup4==4.9.3', 'lxml==4.6.3', 'python-dateutil==2.8.1',
                      'requests==2.25.1', 'pathvalidate==2.4.1', 'jinja2==2.11.3', 'xhtml2pdf==0.2.5',
                      'colorlog==5.0.1', 'Pygments==2.9.0', 'ddt==1.4.2', 'pytest==6.2.4', 'pytest-cov==2.12.1'],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'rss_reader = rss_reader.rss_reader:main',
        ]
    }
)
