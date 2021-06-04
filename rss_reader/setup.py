import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
with open("LICENSE", "r", encoding="utf-8") as fh
    license = fh.read

setuptools.setup(
    name="rss-reader-UrekMazin0",
    version="0.1",
    author="Ivan Rostov-Repin",
    author_email="rostov.repin99@gmail.com",
    description="Simpl python command-line RSS-reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = license
    url="https://github.com/UrekMazin0/PythonFinalTask/tree/main/rss_reader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["urllib==1.26.4", "argparse==1.4.0", "beautifulsoup4==4.9.3"]
    entry_points={
        "console_scripts": [
            'rss_reader=src.reader:main'
            ]
        }
) 
