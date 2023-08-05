import os
import json
from typing import Dict, List, Optional, Tuple
from setuptools import setup, find_packages


BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_readme():
    with open("README.md", "r") as file:
        return file.read()


def get_metadata(overwrite_version: Optional[int] = None) -> Tuple[str, Dict]:
    metadata_path = os.path.join(BASE_PATH, "src/runtime/runtime-metadata.json")
    with open(metadata_path, "r") as file:
        metadata = json.loads(file.read())
    current_build_version = overwrite_version or metadata["current_build"]
    return current_build_version, metadata.get("supported_runtimes", {}).get(current_build_version)


def get_requirements(key: str) -> List[str]:
    # Read dependencies json file
    with open("dependencies.json", "r") as file:
        dependencies = json.loads(file.read())
    # Build requirements list
    return [
        requirement
        for _, values in dependencies.get(key, {}).items()
        for requirement in values
    ]


def get_python_versions(python_version: str) -> Tuple[str, str]:
    major, minor, patch = python_version.split(".")
    return f"{major}.{minor}", f"{major}.{int(minor) + 1}"


RUNTIME_README = get_readme()
RUNTIME_VERSION, RUNTIME_METADATA = get_metadata()
RUNTIME_REQUIREMENTS = get_requirements(key=RUNTIME_VERSION)
RUNTIME_PYMIN, RUNTIME_PYMAX = get_python_versions(python_version=RUNTIME_METADATA["python_version"])

setup(
    name="databricks-runtime",
    version=f"{RUNTIME_VERSION}.dev4",
    description="Databricks LTS Python Runtime",
    long_description=RUNTIME_README,
    long_description_content_type='text/markdown',
    author="rhdzmota",
    author_email='contact@rhdzmota.com',
    url="https://github.com/rhdzmota/databricks-runtime",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    package_dir={
        "": "src"
    },
    package_data={
        "": [
            "runtime/runtime-metadata.json"
        ]
    },
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=RUNTIME_REQUIREMENTS,
    python_requires=f">={RUNTIME_PYMIN}, <{RUNTIME_PYMAX}",
    license="MIT",
)
