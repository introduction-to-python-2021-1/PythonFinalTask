from setuptools import setup

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="rss_reader",
    version="3.0",
    description="Pure Python command-line RSS reader.",
    long_description=readme,
    url="https://github.com/egor-makhlaev/PythonFinalTask/tree/final-task-implementation",
    author="Egor Makhlaev",
    author_email="egor.makhlaev@gmail.com",
    license=license,
    packages=["rss_reader"],
    package_data={
        "rss_reader": ["data/**/*"]
    },
    install_requires=["dateparser", "Jinja2", "pathvalidate", "xhtml2pdf"],
    entry_points={
        "console_scripts": [
            'rss_reader=rss_reader.rss_reader:main',
        ],
    }
)
