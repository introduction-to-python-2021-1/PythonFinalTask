from setuptools import setup, find_packages

setup(
    name='rss_reader',
    version='1.0',
    description='Python RSS-reader',
    url='https://github.com/Yarshou/PythonFinalTask',
    author='Yarshou Daniil',
    author_email='dershov03@gmail.com',
    license='EPAM',
    classifiers=[
        'Development Status :: 5 - Stable',

    ],
    packages=find_packages(),
    install_requires=[
        'pycodestyle==2.4.0',
        'nose==1.3.7',
        'coverage==4.5.1',
        'termcolor==1.1.0',
        'feedparser~=6.0.2',
        'requests~=2.25.1',
    ],
    entry_points={
        'console_scripts': [
            'rss_reader=src.rss_reader:main',
        ]
    },
)
