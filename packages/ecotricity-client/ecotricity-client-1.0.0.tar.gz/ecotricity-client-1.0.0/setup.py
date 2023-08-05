import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

VERSION = "1.0.0"
LONG_DESCRIPTION = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="ecotricity-client",
    version=VERSION,
    author="Derek Kaye",
    description="Wrapper around the Ecotricity API",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dezzak/ecotricity-client"
)
