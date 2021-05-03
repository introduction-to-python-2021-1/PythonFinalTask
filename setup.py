from setuptools import setup


def get_requirements():
    with open('requirements.txt', 'r') as file:
        requirements = file.read().split()
        return requirements


setup(
    name='rss-reader',
    version='0.2',
    description='Command-line RSS reader',
    author='Sergey Rutkovskiy',
    url='https://github.com/spectraise/PythonFinalTask',
    package='src',
    install_requires=get_requirements(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'rss_reader = src.rss_reader:main',
        ]
    }
)
