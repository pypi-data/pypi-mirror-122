import os
import setuptools

_VERSION = "1.0.0"

DEPENDENCY_LINKS = [

]

REQUIRED_PACKAGES = [
    "halo",
    "colorlog",
    "prettytable",
    "innocuousbook-api"
]

setuptools.setup(
    name="innocuousbook_cli",
    version=_VERSION,
    description="Innocuous Book CLI",
    install_requires=REQUIRED_PACKAGES,
    dependency_links=DEPENDENCY_LINKS,
    packages = ["innocuousbook_cli"],
    zip_safe = False,
    author="mao",
    author_email="",
    url="",
    keywords=["innocuousbook"],
    entry_points={
        'console_scripts': [
            'innocuousbook = innocuousbook_cli.innocuousbook:main' 
        ]
    }
)
