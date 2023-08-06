from setuptools import setup, find_packages

setup(
    name='g18nex',
    version='1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'geos18-nexrad-package=geos18_nexrad_package.cli:app',
        ],
    },
    install_requires=[
        "numpy",
        "pandas",
        "typer",
        "requests",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
