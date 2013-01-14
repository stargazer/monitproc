from setuptools import setup, find_packages

setup(
	name = "webserver-monitor",
	version = "0.1",
	packages = find_packages(),
	install_requires=(
		'setuptools',
		'psutil',
	),
)
