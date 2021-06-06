"""
Setup file for the PyMarkdown project.
"""

import os
import runpy
from distutils import util

from setuptools import setup

PROJECT_README_FILE = "README.md"
ALTERNATE_PYPI_README_FILE = "pypi.md"
INSTALL_REQUIREMENT_FILE = "install-requirements.txt"


def parse_requirements():
    lineiter = (line.strip() for line in open(INSTALL_REQUIREMENT_FILE, "r"))
    return [line for line in lineiter if line and not line.startswith("#")]


def get_semantic_version():
    version_meta = runpy.run_path(f"./{PACKAGE_NAME}/version.py")
    return version_meta["__version__"]


def load_readme_file():
    source_file = (
        ALTERNATE_PYPI_README_FILE
        if os.path.exists(ALTERNATE_PYPI_README_FILE)
        else PROJECT_README_FILE
    )
    with open(source_file, "r") as readme_file:
        return readme_file.read()


def ensure_scripts(linux_scripts):
    """
    Creates the proper script names required for each platform (taken from PyLint)
    """
    if util.get_platform()[:3] == "win":
        return linux_scripts + [script + ".bat" for script in linux_scripts]
    return linux_scripts


AUTHOR = "Jack De Winter"
AUTHOR_EMAIL = "jack.de.winter@outlook.com"
PROJECT_URL = "https://github.com/jackdewinter/application_properties"

PACKAGE_NAME = "application_properties"
SEMANTIC_VERSION = get_semantic_version()
MINIMUM_PYTHON_VERSION = "3.8.0"

ONE_LINE_DESCRIPTION = "A prop."
LONG_DESCRIPTION = load_readme_file()
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

KEYWORDS = ["properties"]
PROJECT_CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

PACKAGE_MODULES = [
    "application_properties",
]

setup(
    name=PACKAGE_NAME,
    version=SEMANTIC_VERSION,
    python_requires=">=" + MINIMUM_PYTHON_VERSION,
    install_requires=parse_requirements(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=PROJECT_URL,
    description=ONE_LINE_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    keywords=KEYWORDS,
    classifiers=PROJECT_CLASSIFIERS,
    packages=PACKAGE_MODULES,
    data_files=[
        (
            "Lib/site-packages/pymarkdown/resources",
            ["pymarkdown/resources/entities.json"],
        )
    ],
)
