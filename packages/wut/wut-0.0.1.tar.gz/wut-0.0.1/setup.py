import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
	name='wut',
  version='0.0.1',
  description='Python Web Utilities',
  author='ninjamar',
  url='https://ninjamar.github.io/wut',
  packages=['wut'],
	long_description=long_description
)