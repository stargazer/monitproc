from setuptools import setup, find_packages

setup(
	name = "webserver-monitor",
	version = "0.1",
	packages = find_packages('src'),
	package_dir = {'': 'src'},
	install_requires = [
		'setuptools',
		'psutil',
	],
	entry_points = """
	[console_scripts]
	monitor = monitor.monitor:main
	""",
)
