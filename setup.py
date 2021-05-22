from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in expense_management/__init__.py
from expense_management import __version__ as version

setup(
	name='expense_management',
	version=version,
	description='Expence Management App',
	author='Eco Data',
	author_email='rk@whitehatglobal.org',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
