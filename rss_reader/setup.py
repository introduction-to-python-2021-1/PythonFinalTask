import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()
    
with open("LICENSE", "r", encoding="utf-8") as lic:
    license = lic.read

setuptools.setup(
    name="rss-reader-UrekMazin0",
    version="0.1",
    author="Ivan Rostov-Repin",
    author_email="rostov.repin99@gmail.com",
    description="Simpl python command-line RSS-reader",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license = open("LICENSE").read(),
    url="https://github.com/UrekMazin0/PythonFinalTask/tree/main/rss_reader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["urllib==1.26.4", "argparse==1.4.0", "beautifulsoup4==4.9.3",
                      "pycodestyle==2.4.0", "nose==1.3.7", "termcolor==1.1.0", "coverage==4.5.1"],
    entry_points={
        "console_scripts": [
            'rss_reader=src.reader:main'
            ]
        }
) 
