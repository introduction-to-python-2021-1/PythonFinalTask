from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt') as f_obj:
        contents = f_obj.read()
        requirements = contents.split('\n')
    return requirements


setup(
    name='rss-reader',
    version='1.2',
    author='Raman Maladziashyn',
    author_email='maladziashyn@tut.by',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={'console_scripts': ['rss_reader = rss_reader:main',]}
)