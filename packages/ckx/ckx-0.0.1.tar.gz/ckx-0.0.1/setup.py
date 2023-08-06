import os
import re

from setuptools import setup

# Get version
current_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(current_path, "ckx", "__init__.py"), encoding="utf-8") as f:
    output = re.search(r'__version__ = ["\']([^"\']+)', f.read())

    if not output:
        raise ValueError("Error: can't find version in ckx/__init__.py")

    version = output.group(1)


############################################################
# Add all directories in "automations" to the distribution

root = 'ckx'

setup(
    name="ckx",

    author="",
    author_email="",

    version=version,

    description="CK-X",

    license="",

    long_description=open('./README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",

    url="",

    python_requires="", 

    packages=['ckx'],

    include_package_data=False,

    package_data={'ckx':['']},

    entry_points={"console_scripts": [
                      "ckx = ckx.cli:run"
                  ]},

    zip_safe=False,

    keywords=""
)
