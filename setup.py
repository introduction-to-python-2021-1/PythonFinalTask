from setuptools import setup, find_packages


setup(
    name='rss_reader',
    version='1.2',
    packages=find_packages(),
    url='https://github.com/Dmitry-Grapov/PythonFinalTask',
    license='MIT',
    author='Dmitry Grapov',
    author_email='grapovdmitry@gmail.com',
    description='RSS feed console client',
    entry_points={"console_scripts": ["rss_reader=rss_reader.main:main"]},
)
