"""Install jinjatex."""

from setuptools import setup

with open("README.rst", "r") as file:
    DESCRIPTION = file.read()

setup(
    name="jinjatex",
    version='0.1',
    author='Alexander Dietmüller',
    description="A wrapper to easily use Jinja2 for tex-templates.",
    long_description=DESCRIPTION,
    packages=['jinjatex'],
    install_requires=['Jinja2>=2.9.6'],
    url="https://github.com/NotSpecial/jinjatex",
    download_url="https://github.com/NotSpecial/jinjatex/releases/tag/0.1"
)
