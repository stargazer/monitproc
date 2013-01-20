from setuptools import setup, find_packages

setup(
	name = "monitproc",
	version = "0.1",
	packages = find_packages(),
	install_requires=(
		'setuptools',
		'psutil',
	),
    entry_points={
        'console_scripts': (
            'monitproc=monitproc.run:main',
        )
    },        
)
