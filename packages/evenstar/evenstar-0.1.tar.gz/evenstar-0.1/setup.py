import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="evenstar",
    version="0.1",
    author="Yaser Amiri",
    author_email="yaser.amiri95@gmail.com",
    url="https://github.com/Yaser-Amiri/evenstar",
    description="GraphQL query build",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords="graphql",
    zip_safe=False,
    include_package_data=True,
)
