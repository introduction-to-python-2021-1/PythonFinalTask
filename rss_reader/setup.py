from setuptools import setup, find_packages

# with open(join(dirname(dirname(__file__)), 'requirements.txt'), 'r') as file:
#     requirements = file.read().splitlines()

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
    install_requires=['requests==2.25.1',
                      'feedparser==6.0.2',
                      'python-dateutil~=2.8.1',
                      'rootpath~=0.1.1',
                      'Jinja2~=3.0.1',
                      'WeasyPrint~=52.5'
                      ],
)
