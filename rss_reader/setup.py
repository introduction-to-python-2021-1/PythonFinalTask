from setuptools import setup

setup(
    name='rss_reader',
    version='1.8',
    packages=['reader'],
    author='Natallia Patsiomkina',
    author_email='patsiomkina@inbox.ru',
    description='Pure Python command-line RSS reader',
    install_requires=['feedparser==6.0.2', 'dateparser==1.0.0', 'dominate==2.6.0', 'xhtml2pdf==0.2.5',
                      'colored==1.4.2'],
    entry_points={
        'console_scripts': 'rss_reader = reader.rss_reader:main'
    }
)
