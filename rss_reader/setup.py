from setuptools import setup, find_packages

setup(
    name='rss_reader',
    version='0.1',
    description='Pure Python command-line RSS reader.',
    url="https://github.com/YuliyaLit/PythonFinalTask",
    author="Stralchuk Yuliya",
    author_email='Yuliya-litvinko@mail.ru',
    install_requires=['requests', 'beautifulsoup4', 'lxml',  'dateparser==1.0.0', 'xhtml2pdf'],
    python_requires='>=3.8',
    packages=find_packages(include=['rss_reader', 'rss_reader.*']),
    entry_points={
        "console_scripts": [
            "rss_reader=rss_reader.rss_reader:main",
        ],
    },
)
