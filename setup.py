"""Used for packaging and distribution with Distutils."""

from setuptools import setup  # type: ignore

setup(
    extras_require=dict(
        test=["coverage==5.5", "pytest==6.2.4", "pytest-cov==2.12.0"],
        dev=[
            "black==21.5b1",
            "bump2version==1.0.1",
            "check-manifest==0.46",
            "darglint==1.8.0",
            "flake8==3.9.2",
            "flake8-bugbear==21.4.3",
            "flake8-docstrings==1.6.0",
            "flake8-pytest-style==1.4.1",
            "flake8-typing-imports==1.10.1",
            "gitlint==0.15.1",
            "isort==5.8.0",
            "mypy==0.812",
            "mypy-extensions==0.4.3",
            "pre-commit==2.12.1",
            "pre-commit-hooks==3.4.0",
            "pydocstyle==6.0.0",
            "pylint==2.8.2",
            "pyupgrade==2.14.0",
            "twine==3.4.1",
        ],
    ),
)
