from setuptools import setup
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

dependencies =  [
    "colorama==0.4.4",
    "isodate==0.6.0",
    "pyparsing==2.4.7",
    "rdflib==6.0.1",
    "six==1.16.0"
]

setup(
    name='kgdd',
    version='0.1.0',
    install_requires=dependencies,
    package_dir={"":"Src"},
    long_description=long_description,
    url="https://github.com/ccolonna/kgdd",
    long_description_content_type="text/markdown",
    packages = setuptools.find_packages(where="Src"),
    entry_points = {
        'console_scripts': [
            'kgdd = kgdd.__main__:main'
        ]
    },
    python_requires=">=3.5",
)
