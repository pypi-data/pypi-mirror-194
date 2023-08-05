import json
import os
import sys
from setuptools import setup, find_packages


DESCRIPTION = "Some tools including extensions for Jupyter notebooks."

ROOT_DIR = os.path.dirname(__file__)


def read(name):
    """Read file name contents and return it."""
    with open(os.path.join(ROOT_DIR, name)) as fil:
        return fil.read()


with open(os.path.join(ROOT_DIR, "VERSION"), "r") as f:
    VERSION = json.load(f)["version"]


setup(
    name="toolsvanwinkel",
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Jens Vanwinkel",
    author_email="jensvanwinkel@hotmail.be",
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        # like `jupyter nbextension install --sys-prefix`
        ("share/jupyter/nbextensions/writefile", [
            "writefile/static/main.js",
            "writefile/static/writefile.yaml"
        ]),
        # like `jupyter nbextension enable --sys-prefix`
        ("etc/jupyter/nbconfig/notebook.d", [
            "writefile.json"
        ])
    ],
    install_requires=["notebook>=5.3", "jupyter_contrib_nbextensions", "widgetsnbextension"],
    extras_require={},
    zip_safe=False,
)