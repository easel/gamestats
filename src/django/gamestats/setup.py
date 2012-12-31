from setuptools import setup, find_packages

setup(
    entry_points={
        'console_scripts': [
            'logparse = gamestats.eqlog.parser:main',
        ],
    },
    name = "gamestats",
    version = "0.1",
    packages = find_packages(),
    install_requires=['setuptools']
)
