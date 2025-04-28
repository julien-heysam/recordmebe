import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


def parse_requirements(filename: str):
    with open(filename, "r") as file:
        return file.read().splitlines()


setup(
    name="recordmebe",
    version="0.1.0",
    description="A short description of the project.",
    author="Your name (or your organization/company/team)",
    packages=find_packages(),
    include_package_data=True,
    long_description=README,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "recordmebe=src.interface.cli.cli:cli",
        ],
    },
    zip_safe=False,
    license="MIT",
)
