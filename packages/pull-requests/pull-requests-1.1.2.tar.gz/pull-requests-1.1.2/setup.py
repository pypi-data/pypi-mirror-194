from setuptools import setup

long_description = None
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pull-requests",
    version="1.1.2",
    description="A command line interface for creating pull requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hícaro Dânrlley",
    author_email="hdanrlley1@gmail.com",
    packages=["pull_request"],
    install_requires=["requests"],  # external packages as dependencies
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "pull_request = pull_request.main:_main",
        ]
    },
)
