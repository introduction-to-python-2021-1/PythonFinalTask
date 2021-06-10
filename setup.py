from setuptools import setup, find_packages


setup(
    name="rss_reader",
    version="1.3",
    packages=find_packages(),
    url="https://github.com/Dmitry-Grapov/PythonFinalTask",
    license="MIT",
    author="Dmitry Grapov",
    author_email="grapovdmitry@gmail.com",
    python_requires=">=3.8",
    install_requires=["beautifulsoup4==4.9.3", "certifi==2021.5.30", "chardet==4.0.0", "coverage==5.5",
                      "idna==2.10", "lxml==4.6.3", "nose==1.3.7", "requests==2.25.1",
                      "requests-mock==1.9.3", "six==1.16.0", "soupsieve==2.2.1", "urllib3==1.26.5"],
    description="Pure Python command-line RSS reader.",
    entry_points={"console_scripts": ["rss_reader=rss_reader.main:main"]},
)
