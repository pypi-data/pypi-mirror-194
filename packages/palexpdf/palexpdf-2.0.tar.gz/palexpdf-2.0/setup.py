from pathlib import Path
import setuptools


setuptools.setup(
    name="palexpdf",
    version=2.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
