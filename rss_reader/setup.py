from setuptools import setup,find_packages

setup(
        name="rss_reader",
        version='2.0',
        description='',
        py_modules=['rss_reader'],
        author='Aleksandr Remnev',
        author_email='alexremnev2@gmail.com',
        packages=find_packages(),
        zip_safe=False,
        include_package_data=True,
        entry_points={
                'console_scripts': [
                        'rss_reader=rss_reader.rss_reader:main',
                ],
        }

)
 unexpected spaces around keyword / parameter equals

./setup.py:8:17: E251 unexpected spaces around keyword / parameter equals

./setup.py:9:21: E251 unexpected spaces around keyword / parameter equals

./setup.py:9:23: E251 unexpected spaces around keyword / parameter eq
