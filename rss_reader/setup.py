from setuptools import setup

setup(
        name="rss_reader",
        version='2.0',
        description='',
        author='Aleksandr Remnev',
        author_email='alexremnev2@gmail.com',
        packages=['rss_reader'],
        install_requires=['feedparser', 'pandas', ],
        entry_points={
                'console_scripts': [
                        'rss_reader=rss_reader.rss_reader:main',
                ],
        }
)
