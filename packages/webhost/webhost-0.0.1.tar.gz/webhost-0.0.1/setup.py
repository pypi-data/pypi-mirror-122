from setuptools import setup

setup(
	name='webhost',
	version='0.0.1',
	description='WEBHOST is a simple web framework made with python.',
	long_description=open('README.md', 'r').read(),
	long_description_content_type="text/markdown",
	url = 'https://upload.pypi.org/legacy',
	keywords='webhost',
	package_dir={"": "src"},
	install_requires=['Jinja2', 'parse', 'WebOb', 'whitenoise']
)