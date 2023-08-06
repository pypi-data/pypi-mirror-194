import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

NAME = "foc_common"
VERSION = "0.0.5"
DESCRIPTION = "A description"
REQUIRES_PYTHON = ">=3.6.0"


setuptools.setup(
  name=NAME,
  version=VERSION,
  description=DESCRIPTION,
  packages=setuptools.find_packages(),
  package_data={"logger":['logger.py']},
  include_package_data=True,
)