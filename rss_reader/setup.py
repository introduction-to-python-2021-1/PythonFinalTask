from setuptools import setup

setup(
    name='rss_reader',
    version='0.1',
    description='Pure Python command-line RSS reader.',
    url="https://github.com/YuliyaLit/PythonFinalTask",
    author="Stralchuk Yuliya",
    author_email='Yuliya-litvinko@mail.ru',
    install_requires=['requests', 'beautifulsoup4', 'lxml'],
    python_requires='>=3.8',
    packages=['rss_reader'],
    entry_points={
        "console_scripts": [
            "rss_reader=rss_reader.rss_reader:main",
        ],
    },
)