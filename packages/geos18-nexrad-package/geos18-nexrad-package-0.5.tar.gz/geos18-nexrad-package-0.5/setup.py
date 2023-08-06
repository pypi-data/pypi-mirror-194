from setuptools import setup, find_packages

setup(
    name='geos18-nexrad-package',
    version='0.5',
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
        "boto3",
        "datetime",
        "typing; python_version < '3.9'",
        "python-dotenv",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
