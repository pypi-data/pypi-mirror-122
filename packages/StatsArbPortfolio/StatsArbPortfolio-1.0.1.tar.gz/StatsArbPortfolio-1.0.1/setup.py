import pathlib
from setuptools import setup, find_packages
# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()
# This call to setup() does all the work
setup(
	name="StatsArbPortfolio",
	version="1.0.1",
	description="StatsArbML",
	long_description=README,
	long_description_content_type="text/markdown",
	author="Carlos Gustavo Salas Flores",
	author_email="cs582@duke.edu",
	license="MIT",
	classifiers=[
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.7",
	],
	packages=find_packages(),
	# dependencies for installing the package
	install_requires=["numpy", "pandas", "torch", "sklearn", "yfinance", "matplotlib"]
)
