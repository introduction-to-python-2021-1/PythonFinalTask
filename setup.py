import setuptools

setuptools.setup(name='rss-dimer',
                 version='1.1.5',
                 install_requires=['feedparser', 'unidecode'],
                 packages=setuptools.find_packages(),
                 entry_points={'console_scripts': ['rss-dimer = rss_reader.rss_reader:main']}
                 )
