from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

with open('version.txt') as f:
	version = f.read()

long_description = """Welcome to **Virtual**: the Python project that allows you to run an 'operating system'... in your operating system.
Virtual allows developers to built apps easily, and makes it easier for users, too."""

setup(
	name ='virtualpy',
	version =version,
	author ='Dylan Rogers',
	author_email ='opendylan@proton.me',
	url ='https://github.com/opendylan/',
	description ='Virtual: The Python virtualisation software that allows you to create custom systems!',
	long_description = long_description,
	long_description_content_type ="text/markdown",
	license ='MIT',
	packages = find_packages(),
	entry_points ={
		'console_scripts': [
			'vm = virtualpy.virtual:main'
		]
	},
	classifiers =(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
	keywords ='vm virtual machine python py app program sub computer operating system os pc linux mac macos windows',
	install_requires = requirements,
	zip_safe = False
)